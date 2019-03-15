from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')
def multiPointCentroid(feature, parent):
	"""Calculates the average point of a multiPoint"""
	xSum, ySum = 0, 0
	pts = feature.geometry().asGeometryCollection()
	for pt in pts:
		xSum += pt.asPoint().x()
		ySum += pt.asPoint().y()
	xSum = xSum / len(pts)
	ySum = ySum / len(pts)
	result = QgsGeometry().fromWkt('Point('+str(xSum)+' '+str(ySum)+')')
	return result
