from dataclasses import dataclass, field

@dataclass
class Entry:
    term: int
    cmd: int

@dataclass
class Persistent:
    current_term: int = 0
    voted_for: int = 0
    log: list[Entry] = field(default_factory=list)

@dataclass
class Volatile:
    commit_index: int = 0
    last_applied: int = 0

@dataclass    
class VolatileLeader:
    next_index: list[int] = field(default_factory=list)
    match_index: list[int] = field(default_factory=list)

class StateMachine:
    def __init__():
        pass

    def apply(entries):
        pass
