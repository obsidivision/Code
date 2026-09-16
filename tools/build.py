#!/usr/bin/env python3
"""Regenerate every HTML page from the authoring modules in this folder.

    python3 tools/build.py

The published site is plain static HTML with no build step — this script is
only for editing. It exists because each page carries its content twice (Korean
and English) plus shared chrome, which is not something to maintain by hand
across six files.

Where things live:
  _common.py    TOPICS (including the `hidden` flag that drives the nav),
                the L(ko, en) bilingual helper, and the shared head/nav/footer
  page_*.py     one module per page: prose, diagrams and Python samples

Changing which units appear in the nav means editing the TOPICS row here AND
the matching entry in assets/app.js, then re-running this script.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["page_index", "page_sorting", "page_queue",
         "page_linked_list", "page_graph", "page_tree"]

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    for page in PAGES:
        runpy.run_module(page, run_name="__main__")
