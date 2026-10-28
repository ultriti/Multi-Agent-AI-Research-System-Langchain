# ResearchMind

ResearchMind is an AI-assisted web research prototype. It accepts a topic,
gathers news-oriented web results, reads a selected page, drafts a Markdown
report, and returns a separate model-generated critique.

> **Project status:** Prototype. Generated reports are research starting
> points, not verified facts or professional advice. Review the linked sources
> before relying on any claims.

## Problem and solution

Researching a topic can mean switching between search, reading, note-taking,
writing, and review. ResearchMind brings those activities into one browser
workflow and exposes progress through four sequential stages: search, read,
write, and critique.

## Example use cases

- Prepare a short brief on recent news in a technology or industry.
- Build an initial landscape overview before deeper market research.
- Help students or teams orient themselves to a new topic.
- Identify gaps in an AI-drafted report through a separate critique.

These are suitable exploratory uses; the application does not independently
verify facts or citations.

## Features

- Topic input with suggested research prompts.
- Live status for each pipeline stage.
- Markdown report with an introduction, findings, conclusion, and source links.
- Separate critique with a score, strengths, and suggested improvements.
- Copy and download actions for the report.
- About page explaining the workflow.

## Screenshots

| Workflow view | Screenshot |
|---|---|
| Research workspace | ![ResearchMind home screen](docs/screenshots/home.png) |
| Active research progress | ![Pipeline progress](docs/screenshots/pipeline-progress.png) |
| Generated report and export controls | ![Generated report](docs/screenshots/generated-report.png) |
| Critique and score | ![Review tab](docs/screenshots/report-review.png) |
| About and workflow stages | ![About page](docs/screenshots/about.png) |

The report and review screenshots use representative mock content to show the
interface. Actual output depends on the selected topic and external providers.

## Technology stack

| Layer | Technologies | Why they are used |
|---|---|---|
| Frontend | React, Vite, Tailwind CSS | Component-based UI, fast local development, and utility styling. |
| API | Python, FastAPI, Pydantic | Lightweight HTTP API, request validation, and response streaming. |
| Orchestration | LangChain | Tool-enabled search/reader agents and composed writing/review chains. |
| Models | Google Gemini, Groq-hosted model | Model calls for research, page reading, report drafting, and critique. |
| Web research | Firecrawl, Requests, BeautifulSoup | News search and extraction of readable page text. |
| Progress delivery | Server-Sent Events | Streams sequential workflow status to the browser. |
| Report format | Markdown | Readable in the app and portable as a downloadable `.md` file. |

The detailed technology rationale, architecture, setup steps, API reference,
data handling, limitations, and production roadmap are in
[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

## Run locally

The full prerequisites, provider-key setup, and commands are documented in
[the local setup and runbook](PROJECT_DOCUMENTATION.md#11-local-setup-and-runbook).
The application requires backend credentials for Firecrawl, Gemini, and Groq.
Keep those credentials in a local environment file and never commit them.

## Repository

- `backend/` — FastAPI API, research pipeline, agents, and web tools.
- `frontend/` — React application, status UI, report view, and About page.
- `docs/screenshots/` — application screenshots used by this README and the
  project documentation.
