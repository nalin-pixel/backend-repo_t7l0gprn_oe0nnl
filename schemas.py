"""
Database Schemas for MentorAI

Each Pydantic model maps to a MongoDB collection with the lowercase class name.
Examples:
- UserProfile -> "userprofile"
- Task -> "task"
- Note -> "note"
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class UserProfile(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    avatar_url: Optional[str] = Field(None, description="Profile image URL")
    timezone: Optional[str] = Field(None, description="Preferred timezone e.g. Europe/Rome")
    focus_style: Optional[str] = Field(None, description="User focus preference: pomodoro, deepwork, flow")

class Task(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task details")
    due_date: Optional[datetime] = Field(None, description="Due date/time")
    priority: Optional[str] = Field("medium", description="low | medium | high")
    status: str = Field("todo", description="todo | doing | done")
    tags: List[str] = Field(default_factory=list, description="Labels for filtering")

class Note(BaseModel):
    title: str = Field(..., description="Note title")
    content: str = Field(..., description="Raw note content")
    source: Optional[str] = Field(None, description="Where the note came from: lecture, book, idea")

class StudySession(BaseModel):
    mode: str = Field("pomodoro", description="pomodoro | deep | custom")
    duration_min: int = Field(25, ge=1, le=240, description="Minutes planned")
    topic: Optional[str] = Field(None, description="What are you focusing on")
    completed: bool = Field(False, description="Whether session completed")

class Goal(BaseModel):
    title: str = Field(..., description="Goal name")
    description: Optional[str] = Field(None, description="Why it matters")
    target_date: Optional[datetime] = Field(None, description="Target date")
    progress: int = Field(0, ge=0, le=100, description="Progress percent")

class CreativeDraft(BaseModel):
    kind: str = Field("text", description="text | poem | lyrics | concept")
    title: Optional[str] = Field(None)
    body: str = Field("", description="Draft body text")
    tags: List[str] = Field(default_factory=list)

class Motivation(BaseModel):
    text: str = Field(..., description="Motivational quote text")
    author: Optional[str] = Field(None, description="Author if known")
