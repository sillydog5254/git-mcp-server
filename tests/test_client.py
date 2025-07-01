import asyncio
import json
from fastmcp import Client

# The default URL where the Git MCP server is running.
# Note: FastMCP 2.x serves under the /mcp path by default.
SERVER_URL = "http://127.0.0.1:8000/mcp"


async def main():
    """
    Connects to the MCP server and tests its tools.
    """
    print(f"--- Connecting to MCP Server at {SERVER_URL} ---")

    try:
        # Per documentation, use an async context manager to handle the client's lifecycle.
        async with Client(SERVER_URL) as client:
            print("✅ Connection successful. Testing tools...")

            # 1. Test list_branches
            print("\n1. Testing 'list_branches'...")
            branches_result = await client.call_tool("list_branches")
            # The result is a list of TextContent objects, we extract the .text from each.
            branches = [item.text for item in branches_result]  # type: ignore
            print(f"   Branches: {branches}")

            # 2. Test get_current_branch
            print("\n2. Testing 'get_current_branch'...")
            current_branch_result = await client.call_tool("get_current_branch")
            # The result is a list with one item, we get its .text attribute.
            current_branch = current_branch_result[0].text  # type: ignore
            print(f"   Current Branch: {current_branch}")

            # 3. Test get_status
            print("\n3. Testing 'get_status'...")
            status_result = await client.call_tool("get_status")
            status = status_result[0].text  # type: ignore
            print(f"   Status:\n---\n{status}\n---")

            # 4. Test get_commit_log
            print("\n4. Testing 'get_commit_log' with limit=3...")
            # The tool returns a list of TextContent objects, where each .text is a JSON string.
            log_result = await client.call_tool("get_commit_log", {"limit": 3})
            print("   Commit Log:")
            for item in log_result:
                # We parse the JSON string back into a dictionary.
                commit = json.loads(item.text)  # type: ignore
                print(
                    f"     - {commit['sha']}: {commit['message']} ({commit['author']})"
                )

            # 5. Test show_diff
            print("\n5. Testing 'show_diff' for unstaged changes...")
            diff_result = await client.call_tool("show_diff")
            diff = diff_result[0].text if diff_result else ""  # type: ignore
            if diff:
                print(f"   Unstaged Diff:\n---\n{diff}\n---")
            else:
                print("   No unstaged changes found.")

            print("\n🎉 --- All tools tested successfully! ---")

    except Exception as e:
        print(f"\n❌ ERROR: Could not connect to the server or an error occurred.")
        print(f"   Please ensure the server is running at {SERVER_URL}.")
        print(f"   Details: {e}")


if __name__ == "__main__":
    # Run the async main function.
    asyncio.run(main()) 