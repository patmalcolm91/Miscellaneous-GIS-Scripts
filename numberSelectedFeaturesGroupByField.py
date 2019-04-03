"""
Gives sequential numbers to each group of selected features in the active layer
which have a matching value in a specified field.
Written for QGIS 3. Tested in QGIS 2 and 3.
Author: Patrick Malcolm
"""

NUMBER_FIELD = "ID_FIELD"
GROUP_FIELD = "GROUP"

# ===============================================================

layer = qgis.utils.iface.activeLayer()
groupIdx = layer.fields().indexFromName(GROUP_FIELD)

nextNumber = dict()

for feat in layer.selectedFeatures():
    g = feat.attributes()[groupIdx]
    if g not in nextNumber:
        nextNumber[g] = 1
    feat.setAttribute(NUMBER_FIELD, nextNumber[g])
    layer.updateFeature(feat)
    nextNumber[g] += 1
#layer.commitChanges()  # uncomment this to automatically save changes
