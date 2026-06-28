# Pydantic models: ChatRequest, EvalResult
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime

# The chat request model is what vs code will interact with in forefront. It is the minimum criteria for a chat session to start
class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The current prompt given by the user")
    file_path: str | None = Field(None,description="File path of the current file in the code editor")
    session_id: str = Field(..., description="Unique session id of the current chat")
    max_tokens: int = Field(512, ge=1, le=4096, description="Maximum tokens to generate")
    temperature: float = Field(0.7, ge=0.1, le=1.5, description="Sampling temperature")

# The memory entry schema is for The agent to response
class MemoryEntry(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(..., description="Either 'user', 'assistant' or 'system'")
    content: str = Field(...,min_length=1, description="The actual text of the message")
    session_id: str = Field(..., description="Unique session id of the current chat")
    timestamp: str = Field(default_factory=lambda:datetime.now().isoformat(), description="ISO 8601 time format of the current message generation")

# The Eval Result is for the agent to get the evaluation from flake8 warnings or broken code
class EvalResult(BaseModel):
    passed: bool = Field(..., description="True if passed with No errors")
    warnings: list[str] = Field(default_factory=list, description="Error message warnings from flake8")
    file_path: str | None = Field(None,description="File path of the current file in the code editor")
    timestamp: str = Field(default_factory=lambda:datetime.now().isoformat(), description="ISO 8601 time format of the current message generation")


