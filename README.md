# Miscellaneous-GIS-Scripts
Contains python scripts to perform various tasks. Some are written as processing scripts, others are meant to be loaded for use in Expressions (e.g. for use with the Field Calculator), and others are meant to simply be run from the python window in QGIS.

## Aggregate OD Lines
Aggregates Origin-Destination pair lines into groups based on user-supplied polygonal areas.

## Find Minimum Distance
Processing script which returns the minimum distance between two points in a point layer.

## Average of Multipoint
For use in expressions. Returns the average point / centroid of a multipoint geometry.

## Match Abbreviations
For use in expressions. Evaluates if two strings match, taking common German abbreviations for place names and transportation points into account.

## Number Selected Features
Numbers the selected features in the active layer with an increasing index in the specified field.

## Number Selected Features Group By Field
Numbers each group of the selected features in the active layer which have matching group field values with an increasing index in the specified field.
