#!/usr/bin/env python3

import asyncio
import os
from datetime import date
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.streamable_http import streamable_http_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

CLAUDE_MODEL: str ="claude-haiku-4-5"

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.write = None
        self.stdio = None
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
    # methods will go here

    async def connect_to_server(self, url: str):
        """Connect to an MCP server

        Args:
            url: Url to MCP server, e.g. http://localhost:8000/mcp
        """

        # Connect to a streamable HTTP server
        async with streamable_http_client(f"{url}") as (
                read_stream,
                write_stream,
                _,
        ):
            # Create a session using the client streams
            async with ClientSession(read_stream, write_stream) as self.session:
                # Initialize the connection

                await self.session.initialize()
                # List available tools
                tools = await self.session.list_tools()
                print(f"Available tools: {[tool.name for tool in tools.tools]}")

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )
        messages.append({
            "role": "assistant",
            "content": response.content
        })

        # Process response and handle tool calls
        final_text = []

        tool_result_contents = []
        for content in response.content:
            if content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                content = {
                        "type": "tool_result",
                        "tool_use_id": content.id,
                        "content": result.content
                    }
                tool_result_contents.append(content)

        messages.append({
            "role": "user",
            "content": tool_result_contents
        })

        # Get next response from Claude
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                current_date_and_time = date.today()
                response = await self.process_query(f"We have: {current_date_and_time}. Ensure output displays well in terminal. {query}")
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
