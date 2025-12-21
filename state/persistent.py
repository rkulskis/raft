from dataclasses import dataclass, field
from data.entry import Entry

@dataclass
class Persistent:
    current_term: int = 0
    voted_for: int = 0
    log: dict[int, Entry] = field(default_factory=list)
