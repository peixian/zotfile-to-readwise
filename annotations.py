#!/usr/bin/env python

import io
import csv
import sys
import re

def parse_zotero_format(line):
    """
    Takes in a line and returns a page.

    Example:
    "But in Judith Butler's argument that "the people" constitute a performative event, rather than a pre-existing entity, she reminds us that "this performativity is not only speech, but the demands of bodily action, gesture, movement, congregation, persistence, and exposure to possible violence" [Butler 2012: 120]." (Westmoreland 2016:255)

    returns

    <text>, page
    """
    parens = re.match(r"\(.*\)", line)
    try:
        author, date = parens.split(":")
        return line, int(date[:-1])
    except Exception:
        return line, 0


title = input("Title: ")
author = input("Author: ")
print("Enter annotations. Ctrl-D to finish.")
annotations = []
while True:
    try:
        line = input()
    except EOFError:
        break

    if line and "Extracted Annotations" not in line:
        l, location = parse_zotero_format(line)
        annotations.append({
            'Highlight': l,
            'Title': title,
            'Author': author,
            })

output = io.StringIO()
fieldnames = ['Highlight', 'Title', 'Author']
writer = csv.DictWriter(output, fieldnames=fieldnames)
writer.writeheader()
for val in annotations:
    writer.writerow(val)

print(output.getvalue())

with open('output.csv', 'w') as csvfile:
    csvfile.write(output.getvalue())
