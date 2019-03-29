# -*- coding: utf-8 -*-
"""
This script takes OD-Pair lines and aggregates them into zones based on a given polygon layer.
Written for QGIS >= 3.0
Author: Patrick Malcolm
"""
import processing
from qgis.PyQt.QtCore import QVariant
import math

# INPUT SETTINGS
LINE_LAYER = 'Quell-Ziel'  # Input layer containing OD-Pair Flows
FLOW_FIELD = 'magnitude'  # Field in the line layer containing the flows
AGGZONE_LAYER = 'Bezirke' # Input layer containing zones into which to aggregate
AGGZNAME_FIELD = 'NAME'  # Field in zone layer containing the zone name/ID
# OUTPUT SETTINGS
FROM_FIELD = 'Startzelle'  # Desired name of field in output layer
TO_FIELD = 'Zielzelle'  # Desired name of field in output layer
FLOW_FIELD_OUTPUT = 'Personen'  # Desired name of field in output layer
OUTPUT_LINELAYER_NAME = u'grobe Stroeme'  # Desired name of temporary output layer
DISCARD_INTERNAL_TRIPS = True  # If true, trips starting and ending in the same aggregation zone will be ignored


# END OF SETTINGS =============================================================================

def getLayerByName(name):
    layers = QgsProject.instance().mapLayersByName(name)
    if len(layers) > 1:
        print("Warning: more than one layer with given name found. Using first.")
    return layers[0]


zoneLayer = getLayerByName(AGGZONE_LAYER)
zoneNameIdx = zoneLayer.fields().indexFromName(AGGZNAME_FIELD)
lineLayer = getLayerByName(LINE_LAYER)
flowIdx = lineLayer.fields().indexFromName(FLOW_FIELD)


def getContainingZone(pt):
    for feature in zoneLayer.getFeatures():
        if feature.geometry().contains(pt):
            return feature
    return None


# generate OD matrix
print('Generating OD Matrix from Lines and Zones')
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


def findNearestZone(referenceZone, threshold):
    centr = zoneCentroids[referenceZone]
    nearest = None
    nearestDist = threshold+1
    for z in zoneCentroids.keys():
        if z == referenceZone:
            continue
        x1, y1 = zoneCentroids[z].x(), zoneCentroids[z].y()
        x2, y2 = centr.x(), centr.y()
        d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if d < nearestDist:
            nearestDist = d
            nearest = z
    if nearestDist <= threshold:
        return nearest
    else:
        return None


# loop through lines and aggregate the flows
print('Aggregating flows based on zones')
for feature in lineLayer.getFeatures():
    pl = feature.geometry().asPolyline()  # Get the list of points on the line
    if len(pl) == 0:  # If the above line returns empty, try it as a MultLineString
        pl = feature.geometry().asGeometryCollection()[0].asPolyline()
    try:
        startPoint = pl[0]
        endPoint = pl[-1]
    except IndexError as err:
        print('Unable to read geometry!')
        raise(err)
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
print('Writing temporary output layer')
templayer = QgsVectorLayer('linestring?crs=%s' % zoneLayer.crs().authid(), OUTPUT_LINELAYER_NAME, 'memory')
dataProvider = templayer.dataProvider()
dataProvider.addAttributes([QgsField(FROM_FIELD, QVariant.String),
                            QgsField(TO_FIELD,  QVariant.String),
                            QgsField(FLOW_FIELD_OUTPUT, QVariant.Int)])
templayer.updateFields()  # tell the vector layer to fetch changes from the provider
templayer.startEditing()
feat = QgsFeature()
for o in zoneList:
    for d in zoneList:
        if o is None or d is None or odMatrix[o][d] == 0:
            continue
        if o == d and DISCARD_INTERNAL_TRIPS:
            continue
        pt1 = zoneCentroids[o]
        pt2 = zoneCentroids[d]
        feat.setGeometry(QgsGeometry.fromPolylineXY([pt1, pt2]))
        feat.setFields(templayer.fields())
        feat.setAttribute(FROM_FIELD, o)
        feat.setAttribute(TO_FIELD, d)
        feat.setAttribute(FLOW_FIELD_OUTPUT, odMatrix[o][d])
        dataProvider.addFeatures([feat])
templayer.commitChanges()
templayer.updateExtents()
QgsProject.instance().addMapLayer(templayer)
iface.mapCanvas().refresh()
print('done')
