# ArXiv Research MCP Server  

![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python) ![FastMCP](https://img.shields.io/badge/fastMCP-4.0.5%2B-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)  

A lightweight **Model Context Protocol (MCP)** server that brings the full power of the arXiv API directly into Claude Desktop (or any local AI workflow). Search, retrieve, and extract the content of academic papers without leaving your local environment.

---  

## Table of Contents  

- [Description](#description)  
- [Features](#features)  
- [Tech Stack / Built With](#tech-stack--built-with)  
- [Prerequisites & Installation](#prerequisites--installation)  
- [Run Locally / Usage](#run-locally--usage)  
- [API Reference](#api-reference)  
- [Environment Variables](#environment-variables)  
- [Roadmap](#roadmap)  
- [Contributing](#contributing)  
- [Support / FAQ](#support--faq)  
- [License](#license)  
- [Authors & Acknowledgements](#authors--acknowledgements)  

---  

## Description  

The **ArXiv Research MCP Server** is a Python service built on top of **FastMCP**. It registers two MCP‑compatible tools that can be invoked from any MCP‑aware client (e.g., Claude Desktop):

| Tool | What it does |
|------|--------------|
| `get_arxiv` | Searches arXiv for the most recent papers matching a user‑provided topic and returns a formatted list containing title, authors, abstract, PDF link, and publication date. |
| `get_paper_content` | Downloads a PDF from arXiv and extracts plain‑text from the first *N* pages (configurable). |

Running the server locally gives you full control over data, network traffic, and execution environment—ideal for privacy‑focused research pipelines.

---  

## Features  

| ✅ | Feature |
|---|---------|
| **ArXiv Search** | Query by topic, keyword, or author and receive a concise, human‑readable summary of each result. |
| **PDF Extraction** | Download a PDF from arXiv and extract raw text from a configurable number of pages using **PyMuPDF** (`fitz`). |
| **FastMCP Integration** | Implements the MCP protocol, allowing seamless invocation from Claude Desktop or any MCP‑aware client. |
| **Local Execution** | No external servers; runs on your machine with a single `uv` command (or plain Python). |
| **Extensible Architecture** | Adding new tools is as simple as decorating a Python function with `@mcp.tool()`. |
| **Zero Secrets** | The server does not require API keys or other secrets out of the box. |

---  

## Tech Stack / Built With  

- **Language**: Python ≥ 3.13  
- **MCP Framework**: [FastMCP](https://github.com/fastmcp/fastmcp) (`fastmcp>=4.0.5`)  
- **ArXiv API Wrapper**: `arxiv` (used via `fastmcp` client)  
- **PDF Parsing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) (`pymupdf>=1.28.2`)  
- **HTTP Requests**: `requests>=2.34.2`  
- **Dependency Management**: `uv` (`uv_build` backend)  

---  

## Prerequisites & Installation  

1. **Install `uv`** (recommended, fast and deterministic)  

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # macOS alternative
   brew install uv
   ```

2. **Clone the repository**  

   ```bash
   git clone https://github.com/yourusername/arxiv-mcp.git
   cd arxiv-mcp
   ```

3. **Create a virtual environment and install dependencies**  

   ```bash
   uv sync          # creates .venv and installs all runtime deps
   ```

   *If you prefer classic `pip`*  

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r <(uv pip compile pyproject.toml --no-dev)
   ```

4. **(Optional) Install the console script**  

   ```bash
   uv pip install -e .
   # `arxiv-mcp` is now available on your PATH
   ```

---  

## Run Locally / Usage  

### Start the MCP server  

```bash
# Recommended – uses uv to run the module directly
uv run arxiv-mcp          # equivalent to `python -m arxiv_mcp`

# Or with a plain Python interpreter
python -m arxiv_mcp
```

The server starts on the default MCP stdio channel and waits for tool calls from any MCP‑compatible client.

### Calling the tools from Python (for testing)  

```python
from arxiv_mcp import get_arxiv, get_paper_content

# 1️⃣ Search the latest 5 papers about "machine learning"
print(get_arxiv(max_results=5, topic="machine learning"))

# 2️⃣ Extract the first 3 pages of a specific paper
pdf_url = "https://arxiv.org/pdf/2301.01234.pdf"
print(get_paper_content(pdf_url=pdf_url, max_pages=3))
```

When invoked through an MCP client (e.g., Claude Desktop), you only need to reference the tool name; the server handles argument parsing and returns a plain‑text response.

---  

## API Reference  

| Tool | Signature | Description | Returns |
|------|-----------|-------------|---------|
| `get_arxiv` | `get_arxiv(max_results: int, topic: str) -> str` | Searches arXiv for the most recent papers matching *topic* and limits the output to *max_results*. | A formatted string containing title, authors, abstract, PDF link, and publication date for each paper. |
| `get_paper_content` | `get_paper_content(pdf_url: str, max_pages: int) -> str` | Downloads the PDF at *pdf_url* and extracts plain‑text from the first *max_pages* pages (or fewer if the document is shorter). | A string that begins with a short header (total pages, pages displayed) followed by the extracted text of each page. |

**Error handling** – Both tools return a human‑readable error message if the request fails (e.g., network error, invalid URL, or no results).

---  

## Environment Variables  

The server works out‑of‑the‑box without any secrets. If you need to customise behaviour, you can add the following optional variables to a `.env` file and load them with `python-dotenv` (not required for the default setup).

| Variable | Purpose |
|----------|---------|
| `ARXIV_API_BASE_URL` | Override the default arXiv API endpoint (useful for private mirrors). |
| `HTTP_TIMEOUT` | Global HTTP request timeout in seconds (default: `20`). |

---  

## Roadmap  

- [ ] **Caching layer** – Store downloaded PDFs locally to avoid repeated network calls.  
- [ ] **Citation extraction** – Parse the references section and return structured citation data.  
- [ ] **JSON output mode** – Provide a machine‑readable JSON response alongside the plain‑text format.  
- [ ] **Rate‑limit handling** – Implement exponential back‑off and respect arXiv’s usage policies.  
- [ ] **Docker image** – One‑click containerised deployment for CI/CD pipelines or remote servers.  

Contributions that implement any of the above (or any other useful feature) are welcome!

---  

## Contributing  

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feat/your-feature`).  
3. Install development dependencies: `uv sync --dev`.  
4. Write tests (if applicable) and ensure they pass: `uv run pytest`.  
5. Run the formatter/linter: `uv run ruff check .` and `uv run black .`.  
6. Commit your changes with a clear message and open a Pull Request.  

Please keep the public API stable and follow the existing code style.

---  

## Support / FAQ  

**Q: I get `ImportError: No module named 'mcp'`.**  
A: The `fastmcp` dependency provides the `mcp` package. Make sure you have run `uv sync` (or `pip install -r requirements.txt`) inside the virtual environment.

**Q: The server crashes with a `requests.exceptions.Timeout`.**  
A: The default timeout is 20 seconds. You can increase it by setting the `HTTP_TIMEOUT` environment variable or editing the `requests.get(..., timeout=…)` call in `arxiv_mcp.py`.

**Q: How do I retrieve more than 10 pages of a PDF?**  
A: Pass a larger `max_pages` value to `get_paper_content`. The function will automatically cap it at the actual number of pages in the document.

**Q: Can I run this on Windows?**  
A: Yes. All dependencies (including PyMuPDF) provide pre‑compiled wheels for Windows, macOS, and Linux.

**Q: I want to use the server from a different programming language.**  
A: Any language that can speak the MCP protocol over stdio (or the JSON‑over‑HTTP variant that FastMCP also supports) can invoke the tools. Refer to the FastMCP documentation for client‑side examples.

For further assistance, open an issue on GitHub or contact the author at **hajra.khan2108@gmail.com**.

---  

## License  

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---  

## Authors & Acknowledgements  

- **Hajra Khan** – Project lead & primary developer ([@hajraa21](https://github.com/hajraa21))  
- **FastMCP** – The underlying MCP framework that makes tool registration trivial.  
- **arXiv** – For providing the open‑access scholarly API.  
- **PyMuPDF** – For fast and reliable PDF text extraction.  

Special thanks to the Claude Desktop community for inspiring a locally‑run research assistant.  