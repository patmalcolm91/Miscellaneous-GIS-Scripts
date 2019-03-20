"""
Gives sequential numbers to the selected features in the active layer.
Author: Patrick Malcolm
"""

FIELD = "HstNummer"
START_NUMBER = 1179010535

# ===============================================================

layer = qgis.utils.iface.activeLayer()

i = START_NUMBER
for feat in layer.selectedFeatures():
    feat.setAttribute(FIELD, i)
    layer.updateFeature(feat)
    i += 1
layer.commitChanges()