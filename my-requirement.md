# Requirement: Simplified AI Research Assistant – Jupyter Notebook Lab

## 1. Overview

Refactor and simplify the existing repository

into a **simple AI Research Assistant implemented primarily as a Jupyter Notebook**.

The purpose is to create a **midterm laboratory assignment** for the course:

> **Phát triển các hệ thống thông minh – PTIT**

The project should introduce students to:

- Jupyter Notebook
- Python for AI applications
- Large Language Models (LLM)
- Prompt engineering
- Calling an external LLM API
- Calling a web search API
- Combining search results with an LLM
- Generating a simple research summary/report

The project will use **DeepSeek as the LLM provider instead of OpenAI/ChatGPT**.

The implementation must remain **simple and educational**.

It should NOT attempt to reproduce the complete multi-agent architecture of the original repository.

---

# 2. Main Objective

Build a simple system with the following workflow:

```text
User enters a research topic
            ↓
       DeepSeek LLM
            ↓
     Generate search queries
            ↓
       Web Search API
            ↓
     Search results
            ↓
       DeepSeek LLM
            ↓
     Summarize information
            ↓
      Final research report
```

Example:

```text
Input:
"Applications of Artificial Intelligence in Healthcare"

        ↓

DeepSeek generates search queries:

1. AI applications in healthcare
2. AI medical diagnosis
3. AI healthcare challenges

        ↓

Web search

        ↓

Search results

        ↓

DeepSeek summarizes the information

        ↓

Output:

# Research Report

## Introduction
...

## Main Findings
...

## Applications
...

## Challenges
...

## Conclusion
...

## Sources
...
```

---

# 3. Scope

## 3.1 Required Features

### Feature 1 – Input Research Topic

The user can enter a research topic directly inside the Jupyter Notebook.

Example:

```python
topic = "Applications of AI in education"
```

---

### Feature 2 – Generate Search Queries

Use **DeepSeek LLM** to generate a small number of search queries based on the topic.

Example:

```text
Input:
Applications of AI in education

Output:
1. AI applications in education
2. AI personalized learning
3. AI education challenges
```

The system should generate approximately **3 search queries**.

Do NOT implement complex query planning.

---

### Feature 3 – Web Search

Use a web search API to retrieve information for the generated queries.

The original repository uses Tavily.

The simplified project may continue using:

```text
Tavily Search API
```

Recommended:

```text
3 queries
×
3 results/query
=
maximum 9 results
```

The goal is to keep the notebook simple and minimize unnecessary API usage.

---

### Feature 4 – Display Search Results

The notebook should display the retrieved information in a readable format.

Each result should contain at least:

```text
Title
URL
Content / snippet
```

Example:

```text
1. Artificial Intelligence in Education

URL:
https://example.com/...

Summary:
AI is increasingly being used...
```

---

### Feature 5 – Summarize Search Results

Send the collected search results to **DeepSeek**.

The LLM should produce a concise summary.

The prompt should instruct DeepSeek to:

- use information from the provided search results
- avoid inventing facts
- organize information clearly
- identify important findings
- mention source URLs when appropriate

---

### Feature 6 – Generate Final Research Report

Use DeepSeek to generate a simple final report.

Recommended structure:

```markdown
# Research Report

## 1. Introduction

## 2. Main Findings

## 3. Key Applications / Examples

## 4. Challenges and Limitations

## 5. Conclusion

## Sources
```

The report does not need to be academically rigorous.

The objective is to demonstrate:

```text
Search → Understand → Summarize → Generate
```

---

# 4. Jupyter Notebook Requirement

The main deliverable MUST be:

```text
research_assistant.ipynb
```

The notebook should be executable from top to bottom.

Recommended structure:

```text
01. Introduction

02. Install Dependencies

03. Import Libraries

04. Configure API Keys

05. Initialize DeepSeek LLM

06. Define Research Topic

07. Generate Search Queries

08. Search the Web

09. Display Search Results

10. Summarize Search Results

11. Generate Final Report

12. Display Final Report

13. Conclusion
```

Each major step should contain:

1. Short Markdown explanation
2. Python code
3. Example output

---

# 5. Technology Requirements

Use a minimal technology stack.

Recommended:

```text
Python 3.10+
Jupyter Notebook
LangChain
DeepSeek API
Tavily API
python-dotenv
```

The project SHOULD NOT introduce unnecessary frameworks.

---

# 6. DeepSeek LLM Requirement

The project MUST use **DeepSeek instead of OpenAI/ChatGPT**.

Do NOT require:

```text
OPENAI_API_KEY
OpenAI ChatGPT models
```

Use a DeepSeek API key instead.

Environment variable:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The implementation should use a LangChain-compatible DeepSeek/OpenAI-compatible interface where appropriate, while configuring the endpoint and model for DeepSeek.

The exact model name should be configurable rather than hardcoded throughout the notebook.

Example configuration concept:

```python
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

DEEPSEEK_MODEL = os.getenv(
    "DEEPSEEK_MODEL",
    "deepseek-chat"
)
```

If the DeepSeek provider or SDK changes its recommended integration, use the current official integration/API format rather than introducing unnecessary custom wrappers.

---

# 7. DeepSeek Configuration

The project should centralize DeepSeek configuration.

Example:

```python
from dotenv import load_dotenv
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

DEEPSEEK_MODEL = os.getenv(
    "DEEPSEEK_MODEL",
    "deepseek-chat"
)
```

Do not hardcode API keys.

Do not create multiple LLM configurations unless required.

---

# 8. LangGraph Requirement

The original repository uses LangGraph extensively.

For this simplified project:

## LangGraph is NOT required.

Do not implement:

- Multi-agent graph
- Analyst agents
- Subgraphs
- `Send`
- Parallel execution
- Human-in-the-loop
- Complex state machines
- Conditional routing
- LangGraph Studio

The goal is to teach the basic AI application workflow first.

If desired, LangGraph may be introduced as an **optional extension**, but it must not be required for the main implementation.

---

# 9. Multi-Agent Requirement

The original repository contains multiple analyst agents.

The simplified project MUST use only:

```text
One DeepSeek LLM
+
One Web Search Tool
```

Architecture:

```text
             ┌──────────────┐
             │ Research     │
             │ Topic        │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ DeepSeek     │
             │ LLM          │
             │ Query        │
             │ Generation   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Tavily       │
             │ Web Search   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Search       │
             │ Results      │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ DeepSeek     │
             │ LLM          │
             │ Summarizer   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Final        │
             │ Report       │
             └──────────────┘
```

---

# 10. API Key Management

API keys MUST NOT be hardcoded into the notebook.

Use environment variables.

Example `.env`:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional
DEEPSEEK_MODEL=deepseek-chat
```

The notebook may use:

```python
from dotenv import load_dotenv

load_dotenv()
```

The `.env` file MUST be included in `.gitignore`.

Provide:

```text
.env.example
```

containing:

```env
DEEPSEEK_API_KEY=
TAVILY_API_KEY=
DEEPSEEK_MODEL=deepseek-chat
```

---

# 11. Error Handling

Only basic error handling is required.

### Missing DeepSeek API key

Display:

```text
DEEPSEEK_API_KEY is not configured.
Please configure your DeepSeek API key before running the notebook.
```

### Missing Tavily API key

Display:

```text
TAVILY_API_KEY is not configured.
Please configure your Tavily API key before running the notebook.
```

### Search failure

Display a clear error instead of crashing the entire notebook.

### Empty search result

Display:

```text
No search results were found for this query.
```

Do not implement complicated retry or recovery mechanisms.

---

# 12. Code Quality

The implementation should prioritize readability over abstraction.

Avoid creating unnecessary classes such as:

```text
ResearchAgent
AnalystAgent
SearchAgent
ReportAgent
ResearchGraph
```

For this lab, simple Python functions are preferred.

Example:

```python
def generate_queries(topic):
    ...

def search_web(query):
    ...

def summarize_results(results):
    ...

def generate_report(topic, summary):
    ...
```

The goal is for a student to understand the entire system by reading one notebook.

---

# 13. Project Structure

The final repository should be approximately:

```text
research-assistant/
│
├── research_assistant.ipynb
│
├── README.md
│
├── requirements.txt
│
├── .env.example
│
├── .gitignore
│
└── data/
    └── sample_results.json
```

The `data/` directory is optional.

Do NOT create a large application structure.

Avoid:

```text
src/
agents/
graphs/
nodes/
states/
config/
services/
utils/
tests/
...
```

unless genuinely necessary.

The main educational artifact should remain the notebook.

---

# 14. README Requirement

Create a simple README containing:

## Project Description

Explain what the Research Assistant does.

## Features

```text
- Research topic input
- DeepSeek query generation
- Web search
- Search result summarization
- Final report generation
```

## Architecture

Include a simple architecture diagram using Markdown.

## Installation

Example:

```bash
git clone <repository>
cd research-assistant

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## API Keys

Explain how to configure:

```text
DEEPSEEK_API_KEY
TAVILY_API_KEY
```

## Run Notebook

Example:

```bash
jupyter notebook
```

Then open:

```text
research_assistant.ipynb
```

---

# 15. requirements.txt

Keep dependencies minimal.

The final requirements should contain only libraries actually used.

Potential dependencies:

```text
jupyter
python-dotenv
langchain
langchain-community
langchain-openai
tavily-python
```

If the chosen DeepSeek integration has a dedicated package, use it only if actually necessary.

The important requirement is:

> **Do not retain OpenAI-specific dependencies or code simply because they existed in the original repository.**

The implementation must clearly configure the LLM to use DeepSeek.

---

# 16. Educational Requirements

The notebook should contain explanatory Markdown cells.

Students should be able to understand:

### Concept 1 – What is an LLM?

Brief explanation of Large Language Models.

Explain that this project uses **DeepSeek** as the LLM provider.

---

### Concept 2 – What is Prompt Engineering?

Show a simple prompt.

Example:

```text
You are a research assistant.

Given the following research topic:

{topic}

Generate 3 concise web search queries
that will help research this topic.
```

---

### Concept 3 – What is Tool Calling?

Explain that the LLM does not directly browse the Internet.

Instead:

```text
DeepSeek
   ↓
Search Tool
   ↓
Tavily
   ↓
Web Results
   ↓
DeepSeek
```

---

### Concept 4 – Retrieval-Augmented Generation

Introduce a simple concept:

```text
Search external information
        ↓
Provide information to LLM
        ↓
Generate answer
```

No advanced RAG implementation is required.

---

# 17. Example Prompts

## Query Generation

```text
You are a research assistant.

Given the following research topic:

{topic}

Generate 3 concise web search queries that will help
research this topic.

Return only the search queries as a numbered list.
```

---

## Summarization

```text
You are a research assistant.

Based only on the following search results,
produce a concise and factual summary.

Do not invent information that is not supported
by the provided sources.

Research topic:
{topic}

Search results:
{results}
```

---

## Final Report

```text
You are an AI research assistant.

Create a concise research report based only on
the information provided below.

Topic:
{topic}

Research summary:
{summary}

Structure the report as:

1. Introduction
2. Main Findings
3. Key Applications / Examples
4. Challenges and Limitations
5. Conclusion
6. Sources

Do not invent unsupported facts.
```

---

# 18. Output Requirements

When the notebook finishes, it should produce:

```text
Research Topic
       ↓
DeepSeek Search Queries
       ↓
Tavily Search Results
       ↓
DeepSeek Summary
       ↓
DeepSeek Final Research Report
```

The final report should be displayed directly inside Jupyter Notebook.

Optional:

Save the final report to:

```text
research_report.md
```

---

# 19. Constraints

The implementation MUST remain small.

Target:

```text
< 300 lines of Python code
```

Preferably:

```text
100–200 lines
```

The entire notebook should be understandable by a student who has basic knowledge of:

- Python
- APIs
- JSON
- Jupyter Notebook

No advanced AI knowledge should be required.

---

# 20. Features Explicitly Removed From Original Repository

The following features from the original repository should be removed:

```text
❌ Multiple Analyst Personas

❌ Multi-Agent Architecture

❌ Parallel Agent Execution

❌ LangGraph Send

❌ Subgraphs

❌ Human-in-the-loop

❌ Interview Workflow

❌ Complex State Management

❌ LangGraph Studio

❌ Map-Reduce Architecture

❌ Complex Report Generation Pipeline

❌ Advanced Agent Routing

❌ OpenAI / ChatGPT dependency
```

Keep only:

```text
DeepSeek LLM
      +
Web Search
      +
Information Summarization
      +
Report Generation
```

---

# 21. Optional Extension

If the basic notebook is completed successfully, students MAY implement one optional extension.

Choose only one.

### Extension A – LangGraph

Convert the simple pipeline into:

```text
START
 ↓
Generate Queries
 ↓
Search
 ↓
Summarize
 ↓
Generate Report
 ↓
END
```

Use LangGraph only to demonstrate workflow orchestration.

---

### Extension B – Multiple Search Queries

Run 3 queries and combine their results.

---

### Extension C – Export Report

Export the final report to Markdown or PDF.

---

### Extension D – Source Citation

Include source URLs in the final report.

---

# 22. Acceptance Criteria

The project is considered complete when:

- [ ] `research_assistant.ipynb` exists.
- [ ] Notebook can run from top to bottom.
- [ ] User can enter a research topic.
- [ ] DeepSeek generates search queries.
- [ ] Tavily web search is executed.
- [ ] Search results are displayed.
- [ ] DeepSeek summarizes the search results.
- [ ] DeepSeek generates the final research report.
- [ ] API keys are loaded from environment variables.
- [ ] No API keys are committed to Git.
- [ ] README explains installation and usage.
- [ ] `requirements.txt` contains only necessary dependencies.
- [ ] The implementation does not require LangGraph.
- [ ] The implementation does not use multiple agents.
- [ ] OpenAI/ChatGPT is not required.
- [ ] The code is simple enough for a midterm laboratory assignment.
- [ ] The notebook contains explanatory Markdown cells.
- [ ] DeepSeek is clearly identified as the LLM provider.

---

# 23. Expected Final Result

The final project should feel like a **small educational AI application**, not a production-grade AI Agent framework.

Expected architecture:

```text
                    Research Topic
                           │
                           ▼
                  ┌─────────────────┐
                  │    DeepSeek     │
                  │      LLM        │
                  └────────┬────────┘
                           │
                     Search Queries
                           │
                           ▼
                  ┌─────────────────┐
                  │     Tavily      │
                  │   Web Search    │
                  └────────┬────────┘
                           │
                     Search Results
                           │
                           ▼
                  ┌─────────────────┐
                  │    DeepSeek     │
                  │  Summarization  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Final Research  │
                  │     Report      │
                  └─────────────────┘
```

The primary goal is **not to demonstrate advanced LangGraph or Agent engineering**.

The primary goal is to demonstrate that a student can use:

```text
Jupyter Notebook
      +
Python
      +
DeepSeek LLM
      +
Tavily Web Search
```

to build a basic intelligent system.
