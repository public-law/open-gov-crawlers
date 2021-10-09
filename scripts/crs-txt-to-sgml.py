#!/usr/bin/env python3

#
# Convert a CRS .txt file to parseable SGML.
#

import os
import sys
from typing import Final

PROLOG: Final = '<!DOCTYPE CRS SYSTEM "crs.dtd">\n'

ENTITIES: Final = {
    "amp": 38,
    "cir": 8226,
    "commat": 64,
    "hyphen": 45,
    "deg": 176,
    "lsquo": 8216,
    "mdash": 8212,
    "ntilde": 241,
    "percnt": 37,
    "reg": 174,
    "rsquo": 8217,
    "sect": 167,
    "sup2": 178,
    "Uuml": 220,
}


def fix_unencoded_text(line: str) -> str:
    return (
        line.replace("&RE", "&amp;RE")
        .replace("M&S", "M&amp;S")
        .replace("&A ", "&amp;A ")
        .replace(chr(21), "")
    )


def cleanup(line: str) -> str:
    return line.replace("_", "-")


def replace_entities(line: str) -> str:
    for key, value in ENTITIES.items():
        line = line.replace(f"&{key};", f"&#{value};")

    return line


def fix_and_cleanup(line: str) -> str:
    return replace_entities(cleanup(fix_unencoded_text(line)))


TXT_FILE: Final = sys.argv[1]
SGML_FILE: Final = TXT_FILE.replace(".txt", ".sgml")
XML_FILE: Final = SGML_FILE.replace(".sgml", ".xml")
OSX_CMD: Final = (
    f"osx --encoding=UTF-8 --xml-output-option=no-nl-in-tag {SGML_FILE} > {XML_FILE}"
)

print(f"Converting\n  {TXT_FILE=} to\n  {XML_FILE=}...")

# 1. Clean up the text.
with open(TXT_FILE, encoding="utf8") as f:
    cleaned_up = [fix_and_cleanup(line) for line in f.readlines()]

# 2. Add the DOCTYPE declaration.
cleaned_up.insert(0, PROLOG)

# 3. Save the SGML.
with open(SGML_FILE, mode="w", encoding="utf8") as f:
    f.writelines(cleaned_up)

# 4. Convert the SGML to XML.
os.system(OSX_CMD)
