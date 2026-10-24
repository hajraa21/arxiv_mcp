# ArXiv Research MCP Server  

![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python) ![FastMCP](https://img.shields.io/badge/fastMCP-4.0.5%2B-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)  

A **Model Context Protocol (MCP)** server that brings the full power of the arXiv API directly into Claude Desktop (or any local AI workflow). Search, retrieve, and extract the content of academic papers without leaving your local environment.

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

The **ArXiv Research MCP Server** is a lightweight Python service built on top of **FastMCP**. It exposes two MCP‑compatible tools:

1. **`get_arxiv`** – Search arXiv for the latest papers on a given topic and return a concise summary of each result.  
2. **`get_paper_content`** – Download a paper’s PDF via its URL and extract plain‑text from the first *N* pages.

Because the server runs locally (via `uv` or a standard Python interpreter), you keep full control over your data, network traffic, and execution environment—perfect for privacy‑focused research pipelines.

---

## Features  

| ✅ | Feature |
|---|---------|
| **ArXiv Search** | Query by topic, keyword, or author and receive title, authors, abstract, PDF link, and publication date. |
| **PDF Extraction** | Download a PDF from arXiv and extract raw text from a configurable number of pages using PyMuPDF (`fitz`). |
| **FastMCP Integration** | Implements the MCP protocol, allowing seamless invocation from Claude Desktop or any MCP‑aware client. |
| **Local Execution** | No external servers; runs on your machine with a single `uv` command. |
| **Extensible Architecture** | Adding new tools is as simple as decorating a Python function with `@mcp.tool()`. |

---

## Tech Stack / Built With  

- **Language**: Python ≥ 3.13  
- **MCP Framework**: [FastMCP](https://github.com/fastmcp/fastmcp) (`fastmcp>=4.0.5`)  
- **ArXiv API Wrapper**: `arxiv` (built‑in to `fastmcp` client)  
- **PDF Parsing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) (`pymupdf>=1.28.2`)  
- **HTTP Requests**: `requests>=2.34.2`  
- **Dependency Management**: `uv` (`uv_build` backend)  

---

## Prerequisites & Installation  

1. **Install `uv`** (recommended)  

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or, on macOS with Homebrew
   brew install uv
   ```

2. **Clone the repository**  

   ```bash
   git clone https://github.com/yourusername/arxiv-mcp.git
   cd arxiv-mcp
   ```

3. **Install project dependencies**  

   ```bash
   uv sync          # creates a virtual environment and installs all deps
   ```

   *If you prefer `pip`*  

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r <(uv pip compile pyproject.toml --no-dev)
   ```

4. **(Optional) Install the console script**  

   ```bash
   uv pip install -e .
   # Now `arxiv-mcp` is available on your PATH
   ```

---

## Run Locally / Usage  

### Start the MCP server  

```bash
# Using uv (recommended)
uv run arxiv-mcp          # runs the __main__ block in arxiv_mcp.py

# Or directly with Python
python -m arxiv_mcp
```

The server will start and listen on the default MCP stdio channel, ready to accept tool calls from Claude Desktop or any MCP client.

### Example tool calls (Python REPL)  

```python
from arxiv_mcp import get_arxiv, get_paper_content

# 1️⃣ Search the latest 5 papers about "machine learning"
print(get_arxiv(max_results=5, topic="machine learning"))

# 2️⃣ Extract the first 3 pages of a specific paper
pdf_url = "https://arxiv.org/pdf/2301.01234.pdf"
print(get_paper_content(pdf_url=pdf_url, max_pages=3))
```

When invoked through an MCP‑compatible client, you only need to reference the tool name; the server handles argument parsing and returns a plain‑text response.

---

## API Reference  

| Tool | Signature | Description | Returns |
|------|-----------|-------------|---------|
| `get_arxiv` | `get_arxiv(max_results: int, topic: str) -> str` | Searches arXiv for the most recent papers matching *topic*. Limits results to *max_results*. | A formatted string containing title, authors, abstract, PDF link, and publication date for each paper. |
| `get_paper_content` | `get_paper_content(pdf_url: str, max_pages: int) -> str` | Downloads the PDF at *pdf_url* and extracts plain‑text from the first *max_pages* pages (or fewer if the document is shorter). | A string that starts with a summary of the document length followed by the extracted text of each page. |

**Error handling** – Both tools return a human‑readable error message if the request fails (e.g., network error, invalid URL, or no results).

---

## Environment Variables  

The server does **not** require any secret keys or environment variables out of the box. If you decide to add authentication (e.g., for a private arXiv mirror) you can extend the code to read:

| Variable | Purpose |
|----------|---------|
| `ARXIV_API_BASE_URL` | Override the default arXiv API endpoint. |
| `HTTP_TIMEOUT` | Global request timeout (seconds). |

Add them to a `.env` file and load with `python-dotenv` if needed.

---

## Roadmap  

- **[ ]** Add caching layer to avoid repeated downloads of the same PDF.  
- **[ ]** Support citation extraction (reference section parsing).  
- **[ ]** Provide a JSON‑output mode for easier downstream processing.  
- **[ ]** Implement rate‑limit handling and exponential back‑off for the arXiv API.  
- **[ ]** Docker image for one‑click deployment.  

Contributions that implement any of the above (or any other useful feature) are welcome!

---

## Contributing  

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feat/your-feature`).  
3. Install development dependencies: `uv sync --dev`.  
4. Write tests (if applicable) and ensure they pass: `uv run pytest`.  
5. Format code with `ruff` / `black` (configured in `pyproject.toml`).  
6. Submit a Pull Request with a clear description of the change.  

Please follow the existing code style and keep the public API stable.

---

## Support / FAQ  

**Q: I get `ImportError: No module named 'mcp'`.**  
A: Ensure you installed the `fastmcp` dependency (`uv sync`) and that you are running the script inside the virtual environment created by `uv`.

**Q: The server crashes with a `requests.exceptions.Timeout`.**  
A: The default timeout is 20 seconds. Check your internet connection or increase the timeout by modifying the `requests.get(..., timeout=…)` call.

**Q: How do I retrieve more than 10 pages of a PDF?**  
A: Pass a larger `max_pages` value to `get_paper_content`. The function will cap it at the actual number of pages in the document.

**Q: Can I use this on Windows?**  
A: Yes. The only platform‑specific dependency is PyMuPDF, which provides wheels for Windows, macOS, and Linux.

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