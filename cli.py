#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint-rules - offline deterministic code-aware rule packs.

Usage:
  python cli.py error "pasted error / stack trace"
  python cli.py scan  <file.py> [--lang python]
  python cli.py scan  --code "snippet" [--lang python]
  python cli.py esl   "English text to diagnose"      # L1-transfer patterns
  python cli.py rules            # list available rule counts

Zero dependencies, no network. The same rules power the free tier of
https://tools.aicreditsapi.com (which adds an LLM layer for the long tail).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_rules  # noqa: E402


def _read_file(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def cmd_error(args):
    text = args.text
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read()
    if not text:
        print("Provide an error string: lint-rules error \"TypeError: ...\"")
        return 1
    out = lint_rules.decode_error(text)
    print("\n".join(out))
    return 0


def cmd_scan(args):
    if args.code:
        code = args.code
    elif args.file:
        try:
            code = _read_file(args.file)
        except OSError as e:
            print("Cannot read %s: %s" % (args.file, e))
            return 1
    else:
        if not sys.stdin.isatty():
            code = sys.stdin.read()
        else:
            print("Provide --code \"...\" or --file path.py")
            return 1
    out = lint_rules.scan_security(code)
    print("\n".join(out))
    return 0


def cmd_esl(args):
    text = args.text
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read()
    if not text:
        print('Provide English text: lint-rules esl "I am engineer with 5 years experiences"')
        return 1
    print("\n".join(lint_rules.esl_report(text)))
    return 0


def cmd_rules(args):
    print("Error-decode rules : %d" % len(lint_rules.ERRORS))
    print("Security/CWE rules : %d" % len(lint_rules.SECURITY))
    print("ESL->Native rules : %d" % len(lint_rules.ESL))
    langs = {}
    for r in lint_rules.ERRORS:
        langs[r["lang"]] = langs.get(r["lang"], 0) + 1
    print("Languages covered  : " + ", ".join("%s=%d" % (k, v) for k, v in sorted(langs.items())))
    l1 = {}
    for r in lint_rules.ESL:
        if r.get("l1"):
            l1[r["l1"]] = l1.get(r["l1"], 0) + 1
    if l1:
        print("ESL L1 groups      : " + ", ".join("%s=%d" % (k, v) for k, v in sorted(l1.items())))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="lint-rules", description="Offline code-aware rule packs.")
    sub = p.add_subparsers(dest="cmd")

    pe = sub.add_parser("error", help="Decode a pasted error / stack trace")
    pe.add_argument("text", nargs="*", help="Error text (or pipe via stdin)")
    pe.set_defaults(func=cmd_error)

    ps = sub.add_parser("scan", help="Scan code for secrets / CWE patterns")
    ps.add_argument("--file", help="Path to a source file")
    ps.add_argument("--code", help="Inline code snippet")
    ps.add_argument("--lang", default="auto", help="Language hint (informational)")
    ps.set_defaults(func=cmd_scan)

    pe2 = sub.add_parser("esl", help="Diagnose ESL->Native L1-transfer patterns in English text")
    pe2.add_argument("text", nargs="*", help="English text (or pipe via stdin)")
    pe2.set_defaults(func=cmd_esl)

    pr = sub.add_parser("rules", help="List rule counts")
    pr.set_defaults(func=cmd_rules)

    args = p.parse_args(argv)
    if not getattr(args, "cmd", None):
        p.print_help()
        return 1
    args.text = " ".join(getattr(args, "text", [])) if hasattr(args, "text") else None
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
