import asyncio
import os

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter
from langchain_core.messages import AIMessageChunk
from langchain_ollama import ChatOllama


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
    "You are this app's customer-support assistant"
),
        )

        messages = []
        print("Chat started. Type 'exit' or 'quit' to stop.")

        while True:
            try:
                user_text = await asyncio.to_thread(input, "\nYou: ")
            except (EOFError, KeyboardInterrupt):
                print("\nChat ended.")
                break

            if user_text.strip().lower() in {"exit", "quit"}:
                print("Chat ended.")
                break

            if not user_text.strip():
                continue

            messages.append({"role": "user", "content": user_text})
            print("Assistant: ", end="", flush=True)

            latest_state = {"messages": messages}

            async for mode, chunk in agent.astream(
                {"messages": messages},
                stream_mode=["messages", "values"],
            ):
                if mode == "messages":
                    message_chunk, _metadata = chunk

                    if (
                        isinstance(message_chunk, AIMessageChunk)
                        and isinstance(message_chunk.content, str)
                    ):
                        print(message_chunk.content, end="", flush=True)

                elif mode == "values":
                    latest_state = chunk

            print()
            messages = latest_state["messages"]


if __name__ == "__main__":
    asyncio.run(main())