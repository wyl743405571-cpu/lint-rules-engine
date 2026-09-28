# lint-rules-engine

**Deterministic, zero-cost, code-aware rule packs. Offline. No API. No dependencies.**

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
```

## Engine principle (Engram)

> Let deterministic rules absorb the stable, high-frequency patterns; reserve
> the AI for the long tail it is actually good at.

Rule packs are the ~20-25% of complexity best handled by lookup, not
inference. The U-curve: a rules layer is a *complement* to the model, not a
replacement. A rules hit costs ~0 and is 100% explainable; the model is the
fallback for everything ambiguous.

## Contributing

Rules live in `rules.json`. To add one, append to `errors` or `security` with
the same shape, then open a PR. We especially want: more languages, more CWE
coverage, and error families we missed.

## License

MIT. See [LICENSE](LICENSE).
