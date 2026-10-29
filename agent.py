import asyncio
import os

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessageChunk


async def main() -> None:
    model = ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )

    async with MCPAdapter("http://127.0.0.1:8000/mcp") as adapter:
        tools = await adapter.list_tools()

        agent = create_deep_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are a customer-support assistant. "
                "Use get_all_customers when the user asks for customer details."
            ),
        )

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "get all customers data",
                    }
                ]
            }
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())