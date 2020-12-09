#!/usr/bin/env python

import io
import csv
import sys
import re
import requests
from pathlib import Path

def parse_access_token(access_token_path):
    with open(access_token_path, "r") as token:
        t = token.readline()
    return t

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



if __name__ == "__main__":
    home = str(Path.home())
    token = parse_access_token(f"{home}/.readwise")
    print(f"Using token {token}")

    title = input("Title: ")
    author = input("Author: ")
    type = 'article'
    while True:
        print("Type (must be 'book', 'article', or 'podcast'):", end="")
        type = input().rstrip()
        if type in ['book', 'article', 'podcast']:
            break

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
                'text': l,
                'title': title,
                'source_type': type,
                'author': author,
            })

    resp = requests.post(
        url="https://readwise.io/api/v2/highlights/",
        headers={"Authorization": f"Token {token}"},
        json={
            "highlights": annotations
        }
    )
    print(resp)
    print(resp.content)
