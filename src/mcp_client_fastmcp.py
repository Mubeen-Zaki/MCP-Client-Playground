"""
Just a simple client to test connectivity to the MCP server and retrieve tools for exploration of the FastMCP client library.
"""

from fastmcp import Client
import asyncio

from src.constants import STREAMING_MCP_SERVERS
from src.utils.logger import get_logger, setup_logger


setup_logger()
logger = get_logger(__name__)


class FastMCPClient:
    def __init__(self):
        pass
    

    async def create_client(self):
        mcp_server_config = {
            "mcpServers": STREAMING_MCP_SERVERS
        }
        return Client(mcp_server_config)
    
    
    async def connect_to_server(self):
        mcp_client = await self.create_client()
        async with mcp_client:
            logger.info("Connected to MCP server successfully.")
            tools = await mcp_client.list_tools()
            logger.info(f"Retrieved {len(tools)} tools from MCP server.")
            logger.info(f"Tools available: {[tool.name for tool in tools]}")
    

    async def run_mcp_client(self):
        await self.connect_to_server()


if __name__ == "__main__":
    mcp_client = FastMCPClient()
    asyncio.run(mcp_client.run_mcp_client())
