import git
from git import exc
from pathlib import Path
from typing import List, Optional
from .schemas import Commit


class GitService:
    """A service class for interacting with a git repository."""

    def __init__(self, repo_path: str):
        """
        Initializes the GitService.
        Args:
            repo_path: The file path to the git repository.
        """
        repo_path_obj = Path(repo_path).resolve()
        try:
            self.repo = git.Repo(repo_path_obj, search_parent_directories=True)
        except exc.InvalidGitRepositoryError:
            raise ValueError(f"'{repo_path_obj}' is not a valid git repository.")
        except exc.NoSuchPathError:
            raise ValueError(f"The path '{repo_path_obj}' does not exist.")

    def list_branches(self) -> List[str]:
        """Lists all local branches in the repository."""
        return [branch.name for branch in self.repo.branches]

    def get_current_branch(self) -> str:
        """Gets the name of the current active branch."""
        return self.repo.active_branch.name

    def get_status(self) -> str:
        """Returns the output of 'git status'."""
        return self.repo.git.status()

    def get_commit_log(self, limit: int) -> List[Commit]:
        """
        Retrieves a log of the most recent commits.
        Args:
            limit: The maximum number of commits to return.
        Returns:
            A list of Commit objects.
        """
        commits = list(self.repo.iter_commits(max_count=limit))
        results = []
        for c in commits:
            author_name = c.author.name if c.author and c.author.name else "Unknown"
            
            message = c.message
            if isinstance(message, bytes):
                message = message.decode("utf-8", "replace")

            results.append(
                Commit(
                    sha=c.hexsha[:7],
                    author=author_name,
                    date=c.committed_datetime.isoformat(),
                    message=message.strip().split("\n")[0],
                )
            )
        return results

    def show_diff(self, file_path: Optional[str], staged: bool) -> str:
        """
        Shows the git diff for the repository or a specific file.
        Args:
            file_path: The optional path to a file to diff.
            staged: If true, shows the staged diff. Otherwise, shows unstaged diff.
        Returns:
            A string containing the diff output.
        """
        diff_args = ["--staged"] if staged else []
        if file_path:
            diff_args.append("--")
            diff_args.append(file_path)

        return self.repo.git.diff(*diff_args) 