# -*- coding: utf-8 -*-
"""
Performs a fuzzy match test on two strings, taking common German abbreviations for place names and transportation points into account.
For use with QGIS expressions.
Written for QGIS 3
Author: Patrick Malcolm
"""

import re

@qgsfunction(args='auto', group='Fuzzy Matching', usesgeometry=False)
def matchGermanAbbreviations(text1, text2, feature, parent):
    """Returns true if two strings match. Takes German abbreviations into account."""
    if text1 == text2:
            return True
    else:
        escapes = {
            "(": r"\(",
            ")": r"\)"}
        replacements = {
            " ": r"[ \t\n]*",
            "-": r"(-| )",
            "ä": r"(ä|ae)",
            "ö": r"(ö|oe)",
            "ü": r"(ü|ue)",
            "ß": r"(ß|ss)",
            ".": r"(.|[a-zäüöß]*[.]?[ ]*)",
            ",": r"[, ]*",
            "Bf": r"(Bf|Bahnhof)",
            "Hbf": r"(Hbf|Hauptbahnhof|Hauptbf.)"}
        regex2 = "^" + text2 + "$"
        for abbrev in escapes:
            regex2 = regex2.replace(abbrev, escapes[abbrev])
        for abbrev in replacements:
            regex2 = regex2.replace(abbrev, replacements[abbrev])
        if re.match(regex2, text1):
            return True
        regex1 = "^" + text1 + "$"
        for abbrev in escapes:
            regex1 = regex1.replace(abbrev, escapes[abbrev])
        for abbrev in replacements:
            regex1 = regex1.replace(abbrev, replacements[abbrev])
        if re.match(regex1, text2):
            return True
    return False

# print(matchGermanAbbreviations("Bahnhof Straße","Bf.-Str."))
# print(matchGermanAbbreviations("Asbach, (b.Petershausen)","Asbach (b.Petershausen)"))
