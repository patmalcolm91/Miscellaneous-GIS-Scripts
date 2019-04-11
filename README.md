# Miscellaneous-GIS-Scripts
Contains python scripts to perform various tasks. Some are written as processing scripts, others are meant to be loaded for use in Expressions (e.g. for use with the Field Calculator), and others are meant to simply be run from the python window in QGIS.

## Aggregate OD Lines
Aggregates Origin-Destination pair lines into groups based on user-supplied polygonal areas. QGIS 3 processing script.
![Explanation of OD Line Aggregation](images/FlowAggregationIllustration.png)
### Parameters
* OD Line Layer: Layer containing the origin-destination pair lines.
* Flow Field: Field in the line layer which contains the magnitude of the flows.
* Aggregation Zones Layer: Polygon layer containing the zones into which to aggregate the flows.
* Zone Name Field: Field in the zone layer containing a unique name for each zone. This is used to populate the "from" and "to" fields in the output. Optional. If blank, FIDs will be used.
* Centroid Override X and Y: Fields with coordinates to override the zone centroid. Optional. Null field values will be replaced with the centroid coordinate value.
### Outputs
* Aggregated Lines: Lines between zone centroids containing the sum of the aggregated flow lines between the respective zones.
* Zone Centroids: Centroid of the zone layers with all of the zone fields, plus fields showing internal flows and flows into / out of the zone to / from no other zone.
* Ignored Flows: Sum of flows which have no start or end zone, and were therefore ignored completely.

## Find Minimum Distance
Processing script which returns the minimum distance between two points in a point layer. Versions for both QGIS 2 and 3.

## Average of Multipoint
For use in expressions. Returns the average point / centroid of a multipoint geometry. QGIS 3 custom expression function.

## Match German Abbreviations
For use in expressions. Evaluates if two strings match, taking common German abbreviations for place names and transportation points into account. QGIS 3 custom expression function.

## Number Selected Features
Numbers the selected features in the active layer with an increasing index in the specified field. Works in QGIS 2 and 3. Run from Python window while layer editing is enabled.

## Number Selected Features Group By Field
Numbers each group of the selected features in the active layer which have matching group field values with an increasing index in the specified field. Works in QGIS 3. Run from Python window while layer editing is enabled.
