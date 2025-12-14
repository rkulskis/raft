from dataclasses import dataclass, field

@dataclass
class Persistent:
    current_term: int = 0
    voted_for: int = 0
    log: list[Entry] = field(default_factory=list)
