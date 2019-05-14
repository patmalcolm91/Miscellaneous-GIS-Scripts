@qgsfunction(args='auto',group='Geometry')
def overrideLineZCoordinate(geom, newZ, feature, parent):
	"""Returns a matching LineString geometry but with overridden z values)"""
	pts = geom.asGeometryCollection()[0].asPolyline()
	newPts = []
	for pt in pts:
		newPts.append( QgsPoint(pt.x(), pt.y(), float(newZ)) )
	return QgsGeometry.fromPolyline(newPts)
  
