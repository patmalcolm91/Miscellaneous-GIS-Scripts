from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsField, QgsFields, QgsFeature, QgsGeometry, QgsFeatureSink, QgsFeatureRequest, QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterFeatureSource, QgsProcessingOutputNumber, QgsProcessingParameterField, QgsProcessingParameterBoolean, QgsProcessingException)
                       
class FindMinimumDistance(QgsProcessingAlgorithm):
    INPUT = 'Input Layer'
    OUTPUT = 'Minimum Distance'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "Find Minimum Distance"
     
    def tr(self, text):
        return QCoreApplication.translate("FindMinimumDistance", text)
         
    def displayName(self):
        return self.tr("Find Minimum Distance")
 
    def group(self):
        return self.tr("Geometry")
 
    def groupId(self):
        return "geometry"
 
    def shortHelpString(self):
        return self.tr("""
        Finds the minimum distance between two points in the input layer and returns it as a number output.
        """)
 
    def helpUrl(self):
        return "https://qgis.org"
         
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT,
            self.tr(self.INPUT),
            [QgsProcessing.TypeVectorPoint]))
        self.addOutput(QgsProcessingOutputNumber(
            self.OUTPUT,
            self.tr(self.OUTPUT)))
 
    def processAlgorithm(self, parameters, context, feedback):
        ptLayer = self.parameterAsSource(parameters, self.INPUT, context)

        minDist = None
        featureCount = float(ptLayer.featureCount())
        for i,feature in enumerate(ptLayer.getFeatures()):
            feedback.setProgress(i/featureCount*100)
            for other in ptLayer.getFeatures():
                if feature == other:
                    continue
                d = feature.geometry().asPoint().distance(other.geometry().asPoint())
                if (minDist is None or d < minDist) and d > 0:
                    minDist = d

        if minDist is None:
            raise QgsProcessingException("Minimum distance between points could not be calculated.")

 
        return {self.OUTPUT: minDist}
