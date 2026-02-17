import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    # Define server parameters to run server.py using uv
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\n=== Available Tools ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call the summarize_video tool
            video_url = "https://www.youtube.com/watch?v=kCc8FmEb1nY"
            print(f"\n=== Calling summarize_video with {video_url} ===")
            
            # The tool call might take a while since it runs a subprocess
            result = await session.call_tool("summarize_video", arguments={"url": video_url})
            
            print("\n=== Tool Result ===")
            # The result content is a list of TextContent or similar
            for content in result.content:
                if content.type == 'text':
                    print(content.text)
                else:
                    print(content)

if __name__ == "__main__":
    asyncio.run(run())
