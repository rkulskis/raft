from dataclasses import dataclass, field
from data.entry import Entry

@dataclass
class Persistent:
    current_term: int = 0
    voted_for: int = 0
    log: list[Entry] = field(default_factory=lambda: [Entry()])
