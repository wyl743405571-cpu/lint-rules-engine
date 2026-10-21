# Launch kit — where to post & what to say

Goal: drive the first real (developer) users to Lint through dev-community-native
channels. Competitors' first users came from Reddit / HN / GitHub / Dev.to, not
browser extensions. This repo is the wedge. Posting below is the user's voice —
handles/accounts are theirs; the copy is ready.

## 1) Hacker News — Show HN

**Title:** Show HN: A zero-dep, offline rule pack for decoding errors and finding CWE secrets (the open core of a writing tool for devs)

**Body:**
```
I built Lint — AI writing tools for developers (code-aware grammar, paraphraser,
AI detector). Like most LLM tools, the tempting thing is to throw every input at
the model. But ~20-25% of what comes in is the same stable, high-frequency
patterns: the same stack traces, the same hardcoded-key mistakes. Those don't
need a $ model call — they need a lookup.

So I pulled that layer out into a standalone, dependency-free Python package and
open-sourced it:

- 44 error-decode rules (paste a trace, get cause + fix + doc link)
- 27 CWE-aligned security rules (catches AWS/GitHub/Slack keys, shell=True,
  SQL f-strings, verify=False, etc.)
- 78 ESL->Native rules that explain *why* your English reads non-native —
  each rule names the writer's first-language cause (Chinese -> no articles,
  Russian -> article omission + preposition drift, Spanish -> gerund overuse).
  23 of the 78 are explicitly L1-attributed across 14 language groups.

  The ESL pack is the one generic grammar checkers structurally can't do: they
  see "I am engineer" as fine, because it *is* fine in English. The point is
  it isn't what an English native speaker would write, and the rule says so.

Engram principle: let deterministic rules absorb the stable patterns, reserve the
LLM for the long tail. A rule hit is ~0 cost and 100% explainable.

  offline, zero-dep, MIT: https://github.com/wyl743405571-cpu/lint-rules-engine

The hosted version (free, no signup) layers the AI on top for everything the
rules don't catch. Would love feedback on coverage — what error families or CWE
should be in the pack?
```

## 2) Reddit — r/programming

**Title:** I open-sourced the deterministic rule layer behind my dev writing tool (44 error decoders + 27 CWE checks + 78 L1-transfer English rules, zero deps)

**Body:** (same core as Show HN, but drop the "Show HN" framing; lead with the
engineering decision) — paste the Show HN body minus the HN-specific line.

## 3) Reddit — r/Python

**Title:** Offline CLI that decodes Python tracebacks into cause + fix (no API)

**Body:** lead with the 44 error rules, show the `python cli.py error "TypeError:
'NoneType'..."` example, mention it's the free core of a hosted tool, link repo.

## 4) Reddit — r/learnprogramming  (lower friction, high intent)

**Title:** A free tool to explain what your Python/JS error actually means

**Body:** friendly, beginner-angled. "Paste your error, get a plain-English cause
+ fix." Link repo. No hard sell.

## 5) awesome lists (long-tail SEO + trust)

Submit to relevant `awesome-*` lists: awesome-python (security/debugging),
awesome-cli-apps, awesome-static-analysis. One listing = permanent organic
traffic.

## Posting checklist
- [ ] HN Show HN (Tue/Wed 8–9am EST)
- [ ] r/programming
- [ ] r/Python
- [ ] r/learnprogramming
- [ ] GitHub: add to 2–3 awesome lists
- [ ] Dev.to cross-post a technical writeup ("why we open-sourced our rule engine")
- [ ] After launch: watch the hosted tool's `tool_use`/signups for the funnel bump

## Note
Posting is the user's action (their accounts / voice). If you want me to draft the
Dev.to article or schedule the HN/Reddit drafts as files, say so. The repo itself
is already created and pushed.
