"""
Gives sequential numbers to the selected features in the active layer.
Written for QGIS 3. Tested in QGIS 2 and 3.
Author: Patrick Malcolm
"""

FIELD = "ID_FIELD"
START_NUMBER = 1

# ===============================================================

layer = qgis.utils.iface.activeLayer()

i = START_NUMBER
for feat in layer.selectedFeatures():
    feat.setAttribute(FIELD, i)
    layer.updateFeature(feat)
    i += 1
#layer.commitChanges()  # uncomment this to automatically save changes
