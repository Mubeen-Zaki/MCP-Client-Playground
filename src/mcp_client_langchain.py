"""
This module implements a client that connects to a Multi-Server MCP (Multi-Channel Protocol) server using the langchain_mcp_adapters library. The client retrieves available tools from the server, allows the user to input messages, and processes responses from the server, including any tool calls made by the language model (LLM). The client handles tool calls by invoking the appropriate tools on the server and incorporating their responses back into the conversation with the LLM.
"""

from typing import List, Any
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


from src.config import Settings
from src.constants import MCP_SERVERS
from src.utils.logger import setup_logger, get_logger


setup_logger()
logger = get_logger(__name__)

settings = Settings()


async def get_tool_names(tools: List) -> List[str]:
    tool_names = []
    for tool in tools:
        tool_names.append(tool.name)
    return tool_names


def get_mcp_client() -> MultiServerMCPClient:
    mcp_client = MultiServerMCPClient(
        MCP_SERVERS
    )
    return mcp_client


async def call_tools(session: Any, tool_calls: Any) -> Any:
    tool_responses = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call.get("id")
        logger.info(f"Calling tool '{tool_name}' with arguments: {tool_args}")
        response = await session.call_tool(tool_name, tool_args)
        logger.info(f"Received response from tool '{tool_name}': {response}")
        tool_responses.append(
            ToolMessage(
                content=str(response),
                tool_call_id=tool_call_id
            )
        )
    return tool_responses


async def run_mcp_client_session(mcp_client: MultiServerMCPClient):
    async with mcp_client.session("simple_mcp_server") as session:
        logger.info("Connected to MCP server. Retrieving tools...")
        tools = await load_mcp_tools(session)
        tool_names = await get_tool_names(tools)
        logger.info(f"Received tools from server: {tool_names}")
        llm = get_llm(tools)
        messages = []

        while True:
            message = input("Enter your message or enter 'exit' to quit: ")
            if message.lower() == "exit":
                break
            user_message = HumanMessage(content=message)
            messages.append(user_message)
            response = await llm.ainvoke(messages)
            messages.append(response)
            if response and response.tool_calls:
                logger.info(f"LLM made tool calls: {response.tool_calls}")
                tool_responses = await call_tools(session, response.tool_calls)
                messages.extend(tool_responses)
                final_response = await llm.ainvoke(messages)
                messages.append(final_response)
                logger.info(f"Final LLM response after tool call: {final_response.content}")
            elif response and response.content:
                logger.info(f"LLM response: {response.content}")
            else:
                logger.info("LLM did not return a response.")
                break


async def main():
    logger.info("Starting MCP client...")
    mcp_client = get_mcp_client()
    await run_mcp_client_session(mcp_client)


if __name__ == "__main__":
    asyncio.run(main())
