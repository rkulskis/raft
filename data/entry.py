from dataclasses import dataclass, field

@dataclass
class Entry:
    term: int
    command: tuple[str, int]    # e.g. 'a' <- 10
