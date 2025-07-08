import asyncio
import os
import json
from dotenv import load_dotenv

# OpenAIのAPIキーを環境変数や.envから読み込み
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("環境変数 OPENAI_API_KEY が設定されていません")
notion_token = os.getenv("MCP_SECRET")

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# json.dumps で JSON文字列（エスケープ込み）を作成
mcp_headers = json.dumps({
    "Authorization": f"Bearer {notion_token}",
    "Notion-Version": "2022-06-28"
})

server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@notionhq/notion-mcp-server",
        ],
    env={
        #"OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ntn_****\", \"Notion-Version\": \"2022-06-28\" }"
        "OPENAPI_MCP_HEADERS": mcp_headers
    },
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            tools = await load_mcp_tools(session)
            agent = create_react_agent("openai:gpt-4o",tools=tools) #openai
            response = await agent.ainvoke({"messages": [{"role": "user", "content": "ワークスペースにはどういったナレッジがたまっていますか？"}]})
            print(response)

if __name__ == "__main__":
    asyncio.run(main())