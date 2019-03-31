##input_layer=vector
##minimum_distance=output number

import processing
from qgis.core import *
from PyQt4.QtCore import *
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

ptLayer = processing.getObject(input_layer)

minDist = None
featureCount = float(ptLayer.featureCount())
for i,feature in enumerate(ptLayer.getFeatures()):
    progress.setPercentage(i/featureCount*100)
    for other in ptLayer.getFeatures():
        if feature == other:
            continue
        d = feature.geometry().asPoint().distance(other.geometry().asPoint())
        if (minDist is None or d < minDist) and d > 0:
            minDist = d

if minDist is None:
    raise GeoAlgorithmExecutionException("Minimum distance between points could not be calculated.")

minimum_distance = minDist
