# MCP Servers
MCP_SERVERS = {
            "<MCP_SERVER_NAME>": {
                "transport": "stdio",
                "command": "<PATH_TO_MCP_SERVER_PYTHON>",
                "args": ["<PATH_TO_MCP_SERVER_MAIN_PY>"]
            }
        }

STREAMING_MCP_SERVERS = {
    "<MCP_SERVER_NAME>": {
        "transport": "http",
        "url": "http://<HOST>:<PORT>/mcp"
    }
}