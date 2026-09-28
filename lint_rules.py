#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lint deterministic rule packs - offline, zero-cost, no dependencies.

These are the code-aware *deterministic* rules that power the free tier of
https://tools.aicreditsapi.com . They catch known, frequent patterns with
O(1) regex matching: zero API cost, zero hallucination. The hosted product
layers an LLM on top for the long tail; this repo is the open core.

Engine principle (Engram): let deterministic rules absorb the stable,
high-frequency patterns; reserve the AI for the long tail it is actually
good at. The rules below are the ~20-25% of complexity that is best handled
by lookup, not inference.
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_HERE, "rules.json"), encoding="utf-8") as _f:
    _DATA = json.load(_f)

ERRORS = _DATA.get("errors", [])
SECURITY = _DATA.get("security", [])

# Precompile. Original engine used re.I | re.S for every rule.
for _r in ERRORS:
    _r["_re"] = re.compile(_r.get("pattern", ""), re.I | re.S)
for _r in SECURITY:
    _r["_re"] = re.compile(_r.get("pattern", ""), re.I | re.S)


def match_error(text):
    """Return list of matching error-decode rules for a pasted stack trace / error text."""
    if not text:
        return []
    seen = set()
    out = []
    for r in ERRORS:
        if r["_re"].search(text) and r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    return out


def match_security(code):
    """Return list of matching CWE/security rules for a code snippet or file content."""
    if not code:
        return []
    seen = set()
    out = []
    for r in SECURITY:
        if r["_re"].search(code) and r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    return out


def decode_error(text):
    """Human-readable error decode output (list of strings)."""
    hits = match_error(text)
    if not hits:
        return ["No deterministic rule matched. This is a long-tail case the "
                "LLM layer handles at https://tools.aicreditsapi.com/error-decoder"]
    lines = []
    for h in hits:
        lines.append("=== %s (%s) ===" % (h["title"], h["lang"]))
        lines.append("CAUSE : " + h["cause"])
        lines.append("FIX   : " + h["fix"])
        if h.get("ref"):
            lines.append("REF   : " + h["ref"])
        lines.append("")
    return lines


def scan_security(code):
    """Human-readable security scan output (list of strings)."""
    hits = match_security(code)
    if not hits:
        return ["No known secret/CWE pattern matched."]
    lines = []
    for h in hits:
        lines.append("[%s] %s %s" % (h["severity"].upper(), h["id"], h["title"]))
        lines.append("  %s : %s" % (h["cwe"], h["why"]))
        lines.append("  FIX : " + h["fix"])
        lines.append("")
    return lines


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "TypeError: 'NoneType' object has no attribute 'foo'"
    print("\n".join(decode_error(sample)))
