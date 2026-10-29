import asyncio
from fastmcp import Client


async def main() -> None:
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()

        for tool in tools:
            print(tool.name)
            print(tool.description)
            print(tool.input_schema)

        result = await client.call_tool(
            "get_customer",
            {"customer_id": "CUST-001"},
        )

        print(result)


if __name__ == "__main__":
    asyncio.run(main())