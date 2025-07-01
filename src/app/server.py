from typing import List, Optional
from fastmcp import FastMCP
from .schemas import Commit
from .service import GitService

# These will be initialized from main.py
git_service: Optional[GitService] = None
REPO_ERROR: Optional[str] = None

app = FastMCP()

def initialize_git_service(repo_path: str):
    """Initializes the git service with a given repository path."""
    global git_service, REPO_ERROR
    try:
        git_service = GitService(repo_path)
        REPO_ERROR = None
    except ValueError as e:
        git_service = None
        REPO_ERROR = str(e)


def _raise_if_repo_not_valid():
    if REPO_ERROR:
        raise ValueError(f"Git repository is not valid: {REPO_ERROR}")
    if not git_service:
        raise ValueError("Git service is not initialized.")

@app.tool()
def list_branches() -> List[str]:
    """Lists all local branches in the git repository."""
    _raise_if_repo_not_valid()
    assert git_service is not None
    return git_service.list_branches()

@app.tool()
def get_current_branch() -> str:
    """Gets the name of the current active branch in the git repository."""
    _raise_if_repo_not_valid()
    assert git_service is not None
    return git_service.get_current_branch()

@app.tool()
def get_status() -> str:
    """
    Gets the status of the git repository.
    Equivalent to running 'git status'.
    """
    _raise_if_repo_not_valid()
    assert git_service is not None
    return git_service.get_status()

@app.tool()
def get_commit_log(limit: int = 10) -> List[Commit]:
    """
    Retrieves a log of the most recent commits from the repository.
    
    Args:
        limit: The maximum number of commits to retrieve. Defaults to 10.
    """
    _raise_if_repo_not_valid()
    assert git_service is not None
    return git_service.get_commit_log(limit)

@app.tool()
def show_diff(file_path: Optional[str] = None, staged: bool = False) -> str:
    """
    Shows the git diff. If no file path is provided, it shows the diff for the entire repository.
    
    Args:
        file_path: The optional path to a specific file or directory to see the diff for.
        staged: If set to true, shows the staged changes (what's in the index). Defaults to false, showing unstaged changes.
    """
    _raise_if_repo_not_valid()
    assert git_service is not None
    return git_service.show_diff(file_path, staged)
