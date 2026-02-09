# MCP Client Playground

A playground repository to explore and compare **different ways of building MCP (Model Context Protocol) clients in Python**.

This project focuses on understanding how MCP clients can be implemented using:
- Native MCP Python SDK
- FastMCP utilities
- LangChain adapters with LLM integration

The goal is to experiment, compare trade-offs, and learn how MCP can be used to build tool-aware and agentic workflows.

---

## 🧠 What is MCP?

**Model Context Protocol (MCP)** is a protocol that allows LLM-Powered tools and agents to:
- Discover tools exposed by an MCP server
- Invoke those tools in a structured, standardized way
- Build conversational or agent-based workflows on top of backend services

MCP is especially useful for:
- Agentic systems
- Tool calling and orchestration
- LLM + backend integrations

> This repository only contains **client-side implementations**.  
> An MCP server must be running separately to test these clients.

---

## 🎯 Purpose of This Repository

This repo is intentionally a **playground**, not a production SDK.

The main objectives are:
- Understand different MCP client patterns
- Compare SDK-level vs framework-level abstractions
- Experiment with streaming, conversational loops, and tool invocation
- Learn how MCP fits into modern LLM/agent architectures

---

## 🗂️ Project Structure
├── src/
│ ├── mcp_client_fastmcp.py # MCP client using FastMCP utilities
│ ├── mcp_client_langchain.py # MCP client integrated with LangChain + LLM
│ ├── mcp_client_sdk.py # MCP client using the official Python SDK
│ └── constants.py # Server URLs and shared config
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md

---

## 🚀 Client Implementations

### 1. FastMCP Client
- Lightweight and minimal
- Focuses on direct MCP connectivity and tool discovery
- Useful for understanding the MCP protocol without heavy abstractions

### 2. LangChain MCP Client
- Integrates MCP tools into a LangChain workflow
- Uses an LLM to decide when and how to call tools
- Demonstrates agent-style behavior with MCP

### 3. MCP Python SDK Client
- Uses the official MCP Python SDK
- Supports conversational loops and streaming HTTP
- Closest to how production MCP clients may be implemented

---

## 🛠️ Setup & Requirements

### Prerequisites
- Python **3.13+**
- A running **MCP server** (local or remote)

### Install dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

### Configuration

Update the MCP server details in:
```

src/constants.py

````

If you are using the LangChain-based client, set the following environment variables before running:

```bash
export LLM_MODEL_NAME=...
export LLM_API_KEY=...
export LLM_BASE_URL=...
````

---

## ▶️ Running the Clients

You can run each client independently to observe different MCP interaction patterns:

```bash
uv run python src/mcp_client_fastmcp.py
```

```bash
uv run python src/mcp_client_langchain.py
```

```bash
uv run python src/mcp_client_sdk.py
```

Each script demonstrates a different approach to discovering and invoking tools from an MCP server.

---

## ⚠️ Notes & Limitations

* This repository does **not** include an MCP server implementation
* Error handling and logging are intentionally minimal
* The code is exploratory and optimized for learning and experimentation
* Not intended for direct production use without further hardening

---

## 🔮 Future Improvements

* Improved configuration management
* Better error handling and retries
* Test coverage for MCP client behavior
* Examples using real-world MCP servers
* Deeper exploration of streaming and async interaction patterns
* Agent orchestration examples using MCP tools

---

## 📌 Who Is This Repo For?

* Engineers exploring **MCP and agentic workflows**
* Developers integrating **LLMs with backend tools**
* Anyone curious about **different MCP client abstractions and trade-offs**

---
