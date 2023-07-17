#!/usr/bin/env python3

#
# Convert a CRS .txt file to parseable SGML.
#

import os
import sys
from typing import Final

TXT_FILE:  Final = sys.argv[1]
SGML_FILE: Final = TXT_FILE.replace(".txt", ".sgml")
XML_FILE:  Final = SGML_FILE.replace(".sgml", ".xml")

# The osx executable is provided by the open-sp or opensp packages.
OSX_CMD: Final = (
    f"osx --max-errors=20 --encoding=UTF-8 --xml-output-option=no-nl-in-tag {SGML_FILE} > {XML_FILE}"
)

PROLOG: Final = '<!DOCTYPE CRS SYSTEM "crs.dtd">\n'

ENTITIES: Final = {
    "agrave": 224,
    "alpha": 945,
    "amp": 38,
    "bull": 8226,
    "cir": 8226,
    "commat": 64,
    "deg": 176,
    "hyphen": 45,
    "lsquo": 8216,
    "mdash": 8212,
    "ntilde": 241,
    "percnt": 37,
    "reg": 174,
    "rsquo": 8217,
    "sect": 167,
    "square": 9744,
    "sup1": 165,
    "sup2": 178,
    "trade": 8482,
    "Uuml": 220,
}


def fix_unencoded_text(line: str) -> str:
    return (
        line.replace("&RE", "&amp;RE")
        .replace("M&S", "M&amp;S")
        .replace("&A ", "&amp;A ")
        .replace(chr(21), "")
        .replace(chr(12), "")
    )


def cleanup(line: str) -> str:
    """Why is this necessary? The XML might be easier
    to parse if the text was left as-is.
    """
    return line.replace("_", "-")


def replace_entities(line: str) -> str:
    for key, value in ENTITIES.items():
        line = line.replace(f"&{key};", f"&#{value};")

    return line


def fix_and_cleanup(line: str) -> str:
    return replace_entities(cleanup(fix_unencoded_text(line)))


#
# Execution begins here.
#

print(f"\nConverting\n  {TXT_FILE=} to\n  {XML_FILE=}...")

# 1. Clean up the text.
with open(TXT_FILE, encoding='ascii', errors='replace') as f:
    cleaned_up = [fix_and_cleanup(line) for line in f.readlines()]

# 2. Add the DOCTYPE declaration.
cleaned_up.insert(0, PROLOG)

# 3. Save the SGML.
with open(SGML_FILE, mode="w", encoding="utf8") as f:
    f.writelines(cleaned_up)

# 4. Convert the SGML to XML.
print(f"Executing {OSX_CMD}...")
_ = os.system(OSX_CMD)
