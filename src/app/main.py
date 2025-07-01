import os
from dotenv import load_dotenv
from .server import mcp, initialize_git_service

def main():
    """
    Main function to start the MCP server.
    """
    load_dotenv()

    # Initialize the GitService with the path from .env or use current directory
    repo_path = os.getenv("GIT_REPO_PATH", ".")
    initialize_git_service(repo_path)
    print(f"Git repository initialized at: {os.path.abspath(repo_path)}")

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))

    print(f"Starting MCP server on {host}:{port}")
    mcp.run(transport="http",host=host, port=port)  


if __name__ == "__main__":
    main()
