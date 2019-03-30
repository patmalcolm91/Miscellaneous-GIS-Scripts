from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsField, QgsFields, QgsFeature, QgsGeometry, QgsFeatureSink, QgsFeatureRequest, QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterFeatureSource, QgsProcessingParameterFeatureSink, QgsProcessingParameterField, QgsProcessingParameterBoolean, QgsProcessingException)
                       
class AggregateODLines(QgsProcessingAlgorithm):
    LINE_LAYER = 'OD Line Layer'
    FLOW_FIELD = 'Flow Field'
    AGGZONE_LAYER = 'Aggregation Zones Layer'
    AGGZNAME_FIELD = 'Zone Name Field'
    DISCARD_INTERNAL_TRIPS = 'Discard Internal Trips'
    FROM_FIELD = 'From'
    TO_FIELD = 'To'
    OUTPUT_LINELAYER_NAME = 'Aggregated Lines'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Aggregate OD Lines"
     
    def tr(self, text):
        return QCoreApplication.translate("Aggregate OD Lines", text)
         
    def displayName(self):
        return self.tr("AggregateODLines")
 
    def group(self):
        return self.tr("Travel Demand")
 
    def groupId(self):
        return "travelDemand"
 
    def shortHelpString(self):
        return self.tr("Aggregates OD Pair Lines based on supplied zones.")
 
    def helpUrl(self):
        return "https://qgis.org"
         
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.LINE_LAYER,
            self.tr(self.LINE_LAYER),
            [QgsProcessing.TypeVectorLine]))
        self.addParameter(QgsProcessingParameterField(self.FLOW_FIELD,
            self.tr(self.FLOW_FIELD),
            'Flow',
            self.LINE_LAYER,
            QgsProcessingParameterField.Numeric))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.AGGZONE_LAYER,
            self.tr(self.AGGZONE_LAYER),
            [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterField(self.AGGZNAME_FIELD,
            self.tr(self.AGGZNAME_FIELD),
            'Name',
            self.AGGZONE_LAYER,
            QgsProcessingParameterField.String))
        self.addParameter(QgsProcessingParameterBoolean(self.DISCARD_INTERNAL_TRIPS,
            self.tr(self.DISCARD_INTERNAL_TRIPS),
            QVariant(True)))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_LINELAYER_NAME,
            self.tr(self.OUTPUT_LINELAYER_NAME),
            QgsProcessing.TypeVectorAnyGeometry))
 
    def processAlgorithm(self, parameters, context, feedback):
        lineLayer = self.parameterAsSource(parameters, self.LINE_LAYER, context)
        flowField = self.parameterAsString(parameters, self.FLOW_FIELD, context)
        flowIdx = lineLayer.fields().indexFromName(flowField)
        zoneLayer = self.parameterAsSource(parameters, self.AGGZONE_LAYER, context)
        zoneNameField = self.parameterAsString(parameters, self.AGGZNAME_FIELD, context)
        zoneNameIdx = zoneLayer.fields().indexFromName(zoneNameField)
        outputFields = QgsFields()
        outputFields.append(QgsField(self.FROM_FIELD, QVariant.String))
        outputFields.append(QgsField(self.TO_FIELD,  QVariant.String))
        outputFields.append(QgsField(flowField, QVariant.Int))
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT_LINELAYER_NAME, context,
                                               outputFields,
                                               lineLayer.wkbType(), lineLayer.sourceCrs())

        def getContainingZone(pt):
            for feature in zoneLayer.getFeatures():
                if feature.geometry().contains(pt):
                    return feature
            return None

        # generate OD matrix
        feedback.setProgressText("Generating OD matrix from zones")
        zoneList = []
        zoneCentroids = dict()
        for feature in zoneLayer.getFeatures():
            zName = feature.attributes()[zoneNameIdx]
            if zName not in zoneList:
                zoneList.append(zName)
                zoneCentroids[zName] = feature.geometry().centroid().asPoint()
        zoneList.append(None)
        odMatrix = dict()
        for o in zoneList:
            odMatrix[o] = dict()
            for d in zoneList:
                odMatrix[o][d] = 0

        # loop through lines and aggregate the flows
        feedback.setProgressText("Aggregating OD lines")
        nFeat = float(lineLayer.featureCount())
        for i,feature in enumerate(lineLayer.getFeatures()):
            feedback.setProgress(i/nFeat*100)
            pl = feature.geometry().asPolyline()  # Get the list of points on the line
            if len(pl) == 0:  # If the above line returns empty, try it as a MultLineString
                pl = feature.geometry().asGeometryCollection()[0].asPolyline()
            try:
                startPoint = pl[0]
                endPoint = pl[-1]
            except IndexError as err:
                raise QgsProcessingException("Unable to read geometry from line layer.") from err
            flow = feature.attributes()[flowIdx]
            if flow is not None:
                startZone = getContainingZone(startPoint)
                endZone = getContainingZone(endPoint)
                startName, endName = None, None
                if startZone is not None and startZone != '':
                    startName = startZone.attributes()[zoneNameIdx]
                if endZone is not None and endZone != '':
                    endName = endZone.attributes()[zoneNameIdx]
                odMatrix[startName][endName] += flow

        # Write the aggregated lines
        for o in zoneList:
            for d in zoneList:
                if o is None or d is None or odMatrix[o][d] == 0:
                    continue
                if o == d:
                    continue
                pt1 = zoneCentroids[o]
                pt2 = zoneCentroids[d]
                feat = QgsFeature()
                feat.setGeometry(QgsGeometry.fromPolylineXY([pt1, pt2]))
                feat.setFields(outputFields)
                feat.setAttribute(self.FROM_FIELD, o)
                feat.setAttribute(self.TO_FIELD, d)
                feat.setAttribute(flowField, odMatrix[o][d])
                sink.addFeature(feat, QgsFeatureSink.FastInsert)
 
        return {self.OUTPUT_LINELAYER_NAME: dest_id}
