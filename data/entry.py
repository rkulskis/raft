from dataclasses import dataclass, field
import time

@dataclass
class Entry:
    id: int = field(default_factory=lambda: time.time_ns())
    term: int = 0
    command: tuple[str, str] = ("", "")    # e.g. k <- val
