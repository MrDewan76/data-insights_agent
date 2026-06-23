# Data Insights Agent

A multi-agent AI system that answers natural-language questions about world
economic and development data — live from the **World Bank API**, no setup,
no API key for the data itself, no Kaggle download.

Built as a hands-on project to apply production AI system architecture:
orchestration, least-privilege tool use, and observability — not just a
single prompt-and-response wrapper around an LLM.

```
You: Compare GDP growth in India and Brazil from 2015 to 2023

Agent: India's GDP growth significantly outpaced Brazil's over this period...
       [analysis continues with specific figures]

You: Now show that as GDP per capita instead

Agent: [understands "that" refers to the previous comparison, fetches
        per-capita data for the same countries/years]
```

## Why this exists

Most "AI agent" demos are a single model call with a system prompt. This
project is intentionally architected as a **pipeline of scoped agents**,
each with the minimum permissions needed for its job — the same way you'd
design a secure ETL pipeline, applied to LLM agents.

## Architecture

```
User
  |
  v
Orchestrator  ── owns conversation memory across turns
  |              decides: fetch new data, or answer from context already established?
  |
  +──> Query Agent      ── read-only World Bank API access ONLY
  |                         (no write capability exists in the code, not just the prompt)
  |
  +──> Analysis Agent   ── ZERO tool access, reasons only over data it's handed
  |                         (cannot call the API even if instructed to)
  |
  v
Response  (+ observability: tokens, latency, completion rate tracked per call)
```

### Why three agents instead of one

| Agent | Scope | Why scoped this way |
|---|---|---|
| **Orchestrator** | Routes messages, owns memory | Never touches the data API directly |
| **Query Agent** | Read-only World Bank API calls | Cannot write/delete anything — by code, not promise |
| **Analysis Agent** | No tools at all | Cannot be tricked into "fetching more data" because it has no fetch capability to exploit |

This is defense in depth: even if the Orchestrator's routing were manipulated
by an injected instruction in user input, the Query Agent still can't write
to anything, and the Analysis Agent still can't reach any tool. No single
compromised layer can cascade into real damage.

### Observability

Every agent call is tracked in memory with:
- **Tokens consumed** (catches runaway/expensive calls)
- **Latency** (catches stuck agents, slow tool calls)
- **Success/failure** → aggregated into a completion rate

Type `summary` in the CLI at any time to see the session's metrics, or wait for the automatic summary printed on exit.

## Setup

```bash
git clone <this-repo>
cd data-insights-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python main.py
```

No other API key needed — the World Bank API is public and requires no
authentication.

## Example questions to try

- "What's the population trend in Nigeria over the last 20 years?"
- "Compare inflation in the US, UK, and Japan since 2020"
- "Which BRICS country has the highest GDP per capita?"
- "Now break that down by year" *(follow-up — tests conversation memory)*

## What this does NOT do (by design)

- No write access to any external system
- No ability for the Analysis Agent to fetch its own data
- No unscoped tool access — every tool call is tracked and visible in the session summary

## Tech stack

- Python 3.10+
- [Anthropic API](https://docs.claude.com) (Claude Sonnet)
- [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation) (free, public, no auth)

