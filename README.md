# lint-rules-engine

**Deterministic, zero-cost rule packs. Offline. No API. No dependencies.**

**148 rules** across three packs: 44 error-decode, 27 CWE-aligned security, and
**78 ESL->Native L1-transfer** rules that explain *why* a sentence reads non-native.

This is the open core behind [Lint](https://tools.aicreditsapi.com) — a set of
writing/code tools built for developers. The hosted product layers an LLM on
top for the long tail; the rules here are the stable, high-frequency patterns
we absorbed into deterministic lookup so they cost ~nothing and never
hallucinate.

## What's inside

- **44 error-decode rules** — paste a Python/JS/Node/Go error or stack trace, get
  the likely cause + fix + official doc link. Covers `NoneType` attribute
  errors, `ModuleNotFoundError`, circular imports, `ZeroDivisionError`,
  `UnicodeDecodeError`, `externally-managed-environment`, Flask context errors,
  `Cannot read properties of undefined`, `is not a function`, JSON parse errors,
  and more.
- **78 ESL->Native rules (L1-transfer patterns)** — the pack that generic grammar
  checkers structurally cannot do. A Chinese native speaker drops articles
  entirely ("I am engineer"), a Russian speaker omits articles and drifts on
  prepositions, a Spanish speaker overuses gerunds. These are habits carried over
  from a writer's first language, and **each rule names its L1 cause**. 23 of the
  78 rules are explicitly attributed to a specific first language; 14 L1 groups
  are covered (Chinese, Russian, Spanish, Portuguese, French, German,
  Japanese/Korean, Arabic, Arabic/Hebrew, Hindi/Urdu, Vietnamese, Turkish,
  Polish/Czech, Polish/Czech/Slavic). Every hit returns the cause and a concrete
  fix, not just "grammar issue".
- **27 security rules (CWE-aligned)** — scan code for hardcoded secrets
  (AWS/GitHub/Slack/OpenAI/Google keys, private keys), `eval`/`exec` on dynamic
  input, `shell=True`, SQL built by f-string, unsafe `pickle`/`yaml.load`,
  `verify=False`, `innerHTML` with dynamic values, CORS wildcard, weak hashes,
  hardcoded `SECRET_KEY`, and more.

## Why open source it?

Two reasons, both practical:

1. **These rules are lookup, not IP.** They encode well-known failure modes.
   Open-sourcing them builds trust and lets the community extend the pack
   (new languages, new CWE, new error families).
2. **It's the funnel.** The hosted version at
   [tools.aicreditsapi.com](https://tools.aicreditsapi.com) adds the AI layer
   (free, no signup) for everything these rules *don't* catch. If the CLI saves
   you once, the hosted tool is one click away for the rest.

## Install / run

No install needed — it's pure Python stdlib.

```bash
git clone https://github.com/wyl743405571-cpu/lint-rules-engine
cd lint-rules-engine
python cli.py rules
```

## Usage

Diagnose non-native English (L1-transfer):

```bash
python cli.py esl "I am engineer with 5 years experiences"
```

Output names the first-language cause behind each hit:

```
[HIGH] l1-zh-no-article
  ISSUE  : Missing article (Chinese has no 'a/an/the')
  L1     : Chinese native speaker
  FOUND  : I am engineer
  WHY    : Chinese has no article system, so 'a/an/the' get dropped entirely.
  FIX    : Add the article: 'I am a student', 'he is an engineer'.
```

Decode an error:

```bash
python cli.py error "TypeError: 'NoneType' object has no attribute 'foo'"
```

(Pipe works too: `cat trace.log | python cli.py error`)

Scan a file for secrets / CWE:

```bash
python cli.py scan --file app.py
```

Scan an inline snippet:

```bash
python cli.py scan --code "aws_key = 'AKIAIOSFODNN7EXAMPLE'"
```

## Programmatic use

```python
import lint_rules
hits = lint_rules.match_error("TypeError: 'NoneType' object has no attribute 'x'")
for h in hits:
    print(h["title"], "->", h["fix"])

findings = lint_rules.match_security(open("app.py").read())

hits = lint_rules.match_esl("I am engineer with 5 years experiences")
for h in hits:
    print(h["l1"], h["title"], "->", h["fix"])
```

## Engine principle (Engram)

> Let deterministic rules absorb the stable, high-frequency patterns; reserve
> the AI for the long tail it is actually good at.

Rule packs are the ~20-25% of complexity best handled by lookup, not
inference. The U-curve: a rules layer is a *complement* to the model, not a
replacement. A rules hit costs ~0 and is 100% explainable; the model is the
fallback for everything ambiguous.

## Contributing

Rules live in `rules.json` (errors, security) and `esl_rules.json` (ESL->Native).
To add one, append to the relevant list with the same shape, then open a PR.

We especially want:
- **more L1 groups** — the 14 covered are not exhaustive; Portuguese, Dutch,
  Scandinavian, Thai, Vietnamese tonal-transfer patterns are all fair game
- **error families we missed**
- **more CWE coverage**

For ESL rules, please keep the `why` field specific to the first-language
cause, and cite the transfer-error literature where you can (e.g. Odlin,
*Cross-Linguistic Influence in L2*). A rule that says "this is wrong" is worth
less than one that says "this is wrong *because your first language does it this
way*".

## License

MIT. See [LICENSE](LICENSE).
