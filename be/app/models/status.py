from enum import Enum


class Status(str, Enum):
    """공통 Status enum (Task/Project 모두 사용)."""

    TODO = "todo"
    DONE = "done"
    DROPPED = "dropped"
    DEFERRED = "deferred"
