"""
MCP Client SDK Implementation
This module implements a client for connecting to an MCP server, retrieving available tools, and facilitating a conversational interface with the ability to call tools as needed. The client manages conversation history, tool permissions, and integrates with a language model for generating responses and summaries.
"""
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
from contextlib import AsyncExitStack
from typing import Optional, Any
from uuid import uuid4
import asyncio


from src.utils.logger import setup_logger, get_logger
from src.config import Settings
from src.constants import STREAMING_MCP_SERVERS
from src.utils.llm import get_llm

setup_logger()
logger = get_logger(__name__)
settings = Settings()


class MCPClient:
    def __init__(self):
        self.conversation_id = str(uuid4())
        self.session_id = None
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = None
        self.conversation_history = []
        self.messages = []
        self.message_threshold = 20
        self.all_tool_permissions = False
        self.tool_permissions = {}
        self.conversation_summaries = []
    

    async def list_tool_names(self, tools: Any):
        tool_names = []
        for tool in tools:
            tool_names.append(tool.name)
        return tool_names
    

    async def cleanup_session(self):
        if self.session:
            await self.exit_stack.aclose()
            logger.info("MCP session closed.")
        else:
            logger.warning("No active MCP session to close.")
    

    async def initialize_llm_with_tools(self, tools: Any):
        logger.info("Initializing LLM with available tools...")
        tools = [tool.model_dump() for tool in tools.tools]
        self.llm = get_llm(tools)


    def create_human_message(self, content: str) -> dict:
        return {
            "role": "user",
            "content": content
        }
    

    def create_system_message(self, content: str) -> dict:
        return {
            "role": "system",
            "content": content
        }
    

    async def create_tool_response_message(self, content: str, tool_call_id: Optional[str] = None, status: str = "success") -> dict:
        return {
            "status": status,
            "tool_call_id": tool_call_id,
            "type": "tool",
            "content": content
        }
    

    async def compact_conversation_history(self):
        print("*" * 50)
        logger.info("Compacting conversation history...")
        messages_to_summarize = []
        summary_prompt = "Summarize the following conversation between the user and the assistant, including any important context or information that may be relevant for future interactions under 100 words:\n\n"
        messages_to_summarize.append(self.create_system_message(summary_prompt))
        messages_to_summarize.extend(self.messages)
        summary_response = await self.llm.ainvoke(messages_to_summarize)
        summary_content = summary_response.content if summary_response and hasattr(summary_response, "content") else ""
        self.conversation_summaries.append(summary_content)
        self.conversation_history = self.messages.copy()
        self.messages = [summary_response]


    async def call_tool(self, tool_name: str, tool_args: dict, tool_call_id: Optional[str] = None):
        if not self.session:
            logger.debug("No active session to call tools.")
            return None
        logger.info(f"Calling tool '{tool_name}' with arguments: {tool_args}")
        try:
            response = await self.session.call_tool(tool_name, tool_args)
            logger.info(f"Received response from tool '{tool_name}': {response}")
            return await self.create_tool_response_message(str(response), tool_call_id=tool_call_id)
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}': {e}")
            return await self.create_tool_response_message(str(e), status="error", tool_call_id=tool_call_id)


    def take_tool_permissions(self, tool_name: str):
        while True:
            consent = input(f"1. Allow tool call: '{tool_name}'.\n2. Deny tool call: '{tool_name}'.\n3. Allow all tool calls in this session.\n")
            consent = consent.strip()
            if consent not in ["1", "2", "3"]:
                print("Invalid input. Please enter 1, 2, or 3.")
                continue
            if consent == "1":
                self.tool_permissions[tool_name] = True
                return True
            elif consent == "3":
                self.all_tool_permissions = True
                return True
            break
        return False


    async def call_tools(self, tool_calls: Any) -> Any:
        tool_responses = []
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            tool_call_id = tool_call.get("id")
            if self.all_tool_permissions or self.tool_permissions.get(tool_call["name"], False):
                tool_responses.append(
                    asyncio.create_task(self.call_tool(tool_name, tool_args, tool_call_id))
                )
            else:
                if self.take_tool_permissions(tool_name):
                    tool_responses.append(
                        asyncio.create_task(self.call_tool(tool_name, tool_args, tool_call_id))
                    )
                else:
                    logger.info(f"Tool call '{tool_name}' denied by user.")
                    tool_responses.append(
                        asyncio.create_task(
                            self.create_tool_response_message(f"Tool call '{tool_name}' denied by user.", status="error", tool_call_id=tool_call_id)
                        )
                    )
                           
        return await asyncio.gather(*tool_responses)


    async def handle_tool_calls(self, response: Any) -> bool:
        if response and hasattr(response, "tool_calls") and response.tool_calls:
            tool_responses = await self.call_tools(response.tool_calls)
            self.messages.extend(tool_responses)

    
    def check_for_tool_calls(self, response: Any) -> bool:
        if response and hasattr(response, "tool_calls") and response.tool_calls:
            return True
        return False


    async def process_query(self, query: str) -> Any:
        user_prompt = self.create_human_message(query)
        self.messages.append(user_prompt)
        response = await self.llm.ainvoke(self.messages)
        self.messages.append(response)
        if response and hasattr(response, "content") and response.content:
            print("*" * 50)
            logger.info(f"LLM: {response.content}")
        if self.check_for_tool_calls(response):
            await self.handle_tool_calls(response)
            final_response = await self.llm.ainvoke(self.messages)
            self.messages.append(final_response)
            print("*" * 50)
            logger.info(f"LLM: {final_response.content}")


    async def chat_loop(self):
        logger.info("Starting chat loop")
        while True:
            print("*" * 50)
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                logger.info("Exiting chat loop.")
                break
            await self.process_query(user_input)
            if len(self.messages) > self.message_threshold:
                await self.compact_conversation_history()


    async def connect_to_server(self, server_url: str):
        logger.info(f"Connecting to MCP server at {server_url}")
        async with streamable_http_client(server_url) as (read_stream, write_stream, get_session_id):
            self.session_id = get_session_id()
            self.session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
            await self.session.initialize()
            logger.info(f"Connected to MCP server with session ID: {self.session_id}")
            tools = await self.session.list_tools()
            tools_list = await self.list_tool_names(tools.tools)
            logger.info(f"Available tools: {tools_list}")
            await self.initialize_llm_with_tools(tools)
            await self.chat_loop()
            await self.cleanup_session()
            
    
    async def run_mcp_client(self):
        await self.connect_to_server(STREAMING_MCP_SERVERS["simple_mcp_server"]["url"])
        

if __name__ == "__main__":
    mcp_client = MCPClient()
    asyncio.run(mcp_client.run_mcp_client())
