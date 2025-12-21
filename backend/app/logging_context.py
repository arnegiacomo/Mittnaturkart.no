import logging
from contextvars import ContextVar
from typing import Optional

sub_context: ContextVar[Optional[str]] = ContextVar('sub', default=None)

def set_sub(sub: Optional[str]) -> None:
    sub_context.set(sub)

def get_sub() -> Optional[str]:
    return sub_context.get()

def clear_sub() -> None:
    sub_context.set(None)

class SubFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        sub = get_sub()
        record.sub = sub if sub is not None else "-"
        return True
