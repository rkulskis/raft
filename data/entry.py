from dataclasses import dataclass, field

@dataclass
class Entry:
    term: int = 0
    command: tuple[str, int] = ("", 0)    # e.g. 'a' <- 10
