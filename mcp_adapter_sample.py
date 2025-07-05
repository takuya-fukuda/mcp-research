import asyncio
import os
from dotenv import load_dotenv

# OpenAIのAPIキーを環境変数や.envから読み込み
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("環境変数 OPENAI_API_KEY が設定されていません")

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        #"/Users/username/Desktop"
        "/Users/fukuda_takuya/Desktop"
        ],
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            tools = await load_mcp_tools(session)
            #agent = create_react_agent("anthropic:claude-3-7-sonnet-latest",tools=tools)
            agent = create_react_agent("openai:gpt-4o",tools=tools) #openai
            #response = await agent.invoke({"message": "デスクトップに何がある？"})
            #response = agent.invoke({"messages": [{"role": "user", "content": "デスクトップに何がある？"}]})
            response = await agent.ainvoke({"messages": [{"role": "user", "content": "デスクトップに何がある？"}]})
            print(response)

if __name__ == "__main__":
    asyncio.run(main())