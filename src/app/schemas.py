from pydantic import BaseModel


class Commit(BaseModel):
    """Represents a single git commit."""

    sha: str
    author: str
    date: str
    message: str
