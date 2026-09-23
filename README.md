# ArXiv Research MCP Server

A custom Model Context Protocol (MCP) server that integrates ArXiv directly into Claude Desktop, allowing you to search, query, and analyze academic papers seamlessly through local AI workflows.

---

## Features

* **ArXiv Search**: Query academic papers by topic, keywords, or author directly from Claude.
* **FastMCP Powered**: Built using modern `FastMCP` architecture for robust tool execution and local stdio communication.
* **Local Integration**: Runs locally on your machine via Python and `uv`, giving you full control over your research environment.

---

## Project Structure

```text
arxiv-mcp/
├── arxiv_mcp.py        # Main MCP server implementation and ArXiv logic
├── pyproject.toml      # Project configuration and dependency management
├── uv.lock             # Lockfile for reproducible dependencies
└── README.md           # Project documentation
