## About

This project explores MCP client implementations using different libraries and SDKs. It includes:

- FastMCP client for basic connectivity and tool discovery.
- LangChain MCP adapter client for interactive tool calling with an LLM.
- MCP Python SDK client with a conversational loop, tool permissions, and streaming HTTP transport.

## Installation and How to Run

### Prerequisites

- Python 3.13 or newer.
- An MCP server to connect to.

The MCP server configuration is defined in [src/constants.py](src/constants.py). Update the paths and URLs to match your local MCP server setup.

### Setup

1. Install uv (if needed):

```bash
pip install uv
```

2. Create the virtual environment and install dependencies:

```bash
uv sync
```

3. Create a .env file (optional) to configure the LLM used by the LangChain and SDK clients:

```env
LLM_MODEL_NAME=gpt-3.5-turbo
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
```

### Run

Run any client directly:

```bash
uv run python src/mcp_client_fastmcp.py
```

```bash
uv run python src/mcp_client_langchain.py
```

```bash
uv run python src/mcp_client_sdk.py
```

Logs are written to the logs/ directory by default.
