# AI Research Assistant — Jupyter Notebook Lab

> A small educational **AI research assistant** built in a single Jupyter
> Notebook. Given a research topic, it uses **DeepSeek** to generate search
> queries, retrieves web results with **Tavily**, then asks DeepSeek to
> summarize the results and write a short research report.

**Course:** Phát triển các hệ thống thông minh — PTIT (midterm laboratory)

---

## Project Description

This project is a simplified, notebook-first research assistant. It shows the
core workflow of an intelligent system in about 200 lines of Python:

```text
Research topic  ->  DeepSeek generates queries  ->  Tavily web search
                ->  DeepSeek summarizes         ->  DeepSeek writes the report
```

The whole system is **one LLM + one search tool + four small Python functions**.
There is no multi-agent architecture, no LangGraph, and no OpenAI dependency.

The main deliverable is `research_assistant.ipynb`, readable from top to bottom.

---

## Features

- **Research topic input** — set one variable in the notebook.
- **DeepSeek query generation** — the LLM proposes 3 web search queries.
- **Web search** — Tavily returns up to 3 results per query (max 9 results).
- **Search result display** — title, URL and snippet for every result.
- **Summarization** — DeepSeek summarizes only the retrieved content.
- **Final report generation** — a Markdown report with a fixed structure.
- **Source list** — appendix generated from the real URLs (never hallucinated).
- **Report export** — the report is saved to `research_report.md`.
- **DEMO MODE** — the notebook runs end-to-end even without API keys, using
  `data/sample_results.json`, so students can see the expected output first.

---

## Architecture

```text
                 Research Topic (notebook cell 06)
                            |
                            v
                 +---------------------+
                 |  DeepSeek LLM       |   generate_queries()
                 |  Query Generation   |
                 +----------+----------+
                            |  3 search queries
                            v
                 +---------------------+
                 |  Tavily Web Search  |   search_web()
                 |  3 queries x 3 hits |
                 +----------+----------+
                            |  JSON results (title, url, content)
                            v
                 +---------------------+
                 |  DeepSeek LLM       |   summarize_results()
                 |  Summarization      |
                 +----------+----------+
                            |  factual summary
                            v
                 +---------------------+
                 |  DeepSeek LLM       |   generate_report()
                 |  Report Generation  |
                 +----------+----------+
                            |  Markdown report
                            v
              display in notebook  +  research_report.md
```

| Function | Role |
|---|---|
| `generate_queries(topic, n=3)` | asks DeepSeek for search queries |
| `search_web(query, max_results)` | calls the Tavily search API |
| `summarize_results(topic, results)` | asks DeepSeek to summarize the results |
| `generate_report(topic, summary)` | asks DeepSeek to write the report |
| `ask_deepseek(prompt, demo_answer)` | the single LLM call helper |

---

## Project Structure

```text
.
├── research_assistant.ipynb   # the main deliverable (13 sections)
├── README.md                  # this file
├── BAO_CAO_UAT.md             # Vietnamese feature & UAT report
├── HUONG_DAN_PYCHARM.md       # Vietnamese step-by-step PyCharm guide
├── requirements.txt           # minimal dependencies
├── .env.example               # template for API keys
├── .gitignore
└── data/
    └── sample_results.json    # offline sample data used by DEMO MODE
```

---

## Installation

```bash
git clone <repository-url>
cd LangGraph_Research_Assistant_Agent

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Requires **Python 3.10+**.

---

## API Keys

API keys are never written in the notebook. Copy the template and fill it in:

```bash
cp .env.example .env
```

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
TAVILY_API_KEY=your_tavily_api_key
DEEPSEEK_MODEL=deepseek-flash
```

| Variable | Required | Where to get it |
|---|---|---|
| `DEEPSEEK_API_KEY` | yes | <https://platform.deepseek.com/api_keys> |
| `TAVILY_API_KEY` | yes | <https://app.tavily.com/home> |
| `DEEPSEEK_MODEL` | no | defaults to `deepseek-flash` |
| `DEEPSEEK_BASE_URL` | no | defaults to `https://api.deepseek.com` |

`.env` is already listed in `.gitignore`, so keys are never committed.

### DEMO MODE

If one or both keys are missing, the notebook prints a clear message and turns
on **DEMO MODE**. In DEMO MODE the search step reads
`data/sample_results.json` and the LLM steps return pre-written answers, so the
notebook still runs from top to bottom and every cell produces output.

---

## Run the Notebook

```bash
jupyter notebook
```

Then open `research_assistant.ipynb` and use **Cell → Run All**.

> 🧭 **Using PyCharm?** See the Vietnamese step-by-step guide
> [`HUONG_DAN_PYCHARM.md`](HUONG_DAN_PYCHARM.md) — it covers the interpreter,
> Jupyter server/kernel selection, running the notebook and troubleshooting.

---

## Notebook Sections

| # | Section | What it does |
|---:|---|---|
| 01 | Introduction | the 4 concepts: LLM, prompt engineering, tool calling, RAG |
| 02 | Install dependencies | `pip install -r requirements.txt` |
| 03 | Import libraries | 7 imports |
| 04 | Configure API keys | reads `.env`, detects DEMO MODE |
| 05 | Initialize DeepSeek LLM | one `ChatOpenAI` client with the DeepSeek endpoint |
| 06 | Define research topic | edit this one variable |
| 07 | Generate search queries | DeepSeek proposes 3 queries |
| 08 | Search the web | Tavily, max 9 results, basic error handling |
| 09 | Display search results | title, URL, snippet |
| 10 | Summarize results | RAG step: results are inserted into the prompt |
| 11 | Generate final report | fixed Markdown structure |
| 12 | Display and save report | renders the report, appends real sources, writes `.md` |
| 13 | Conclusion | recap, exercises, optional extensions, troubleshooting |

---

## Error Handling

Only basic error handling is implemented, as required:

| Case | Behaviour |
|---|---|
| Missing `DEEPSEEK_API_KEY` | prints `DEEPSEEK_API_KEY is not configured.` and continues in DEMO MODE |
| Missing `TAVILY_API_KEY` | prints `TAVILY_API_KEY is not configured.` and continues in DEMO MODE |
| Search request fails | prints `Search failed for '<query>': <error>` and returns an empty list |
| No results for a query | prints `No search results were found for this query.` |

No retries, no recovery loops.

---

## Tech Stack

| Layer | Tool | Role |
|---|---|---|
| Language | Python 3.10+ | runtime |
| Notebook | Jupyter | the lab itself |
| LLM provider | **DeepSeek** | query generation, summarization, report writing |
| LLM client | `langchain-openai` (`ChatOpenAI`) | OpenAI-compatible client pointed at DeepSeek |
| Web search | Tavily (`tavily-python`) | retrieval |
| Configuration | `python-dotenv` | loads `.env` |

`langchain` and `langgraph` are **not** required. Latent LangGraph is offered
only as an optional exercise in section 13.

---

## Optional Extensions (section 13, choose one)

- **A. LangGraph** — express the pipeline as `START -> ... -> END`.
- **B. More queries** — combine results from 5 queries.
- **C. Export** — save the report as PDF or a timestamped Markdown file.
- **D. Citations** — cite sources inline as `[1]`, `[2]`.

---

## Limitations

- A valid DeepSeek and Tavily API key is needed for real results; otherwise the
  notebook runs in DEMO MODE on synthetic sample data.
- Report quality depends on the topic and on the quality of the search results.
- The generated report is a research draft, not professional advice.
- `deepseek-flash` and `deepseek-v4-pro` are the current official DeepSeek
  model names; older tutorials use the legacy `deepseek-chat`.

---

## License

MIT — free to use, modify and extend for teaching purposes.
