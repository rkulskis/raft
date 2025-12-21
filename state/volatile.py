from dataclasses import dataclass, field

@dataclass
class Volatile:
    commit_index: int = 0
    last_applied: int = 0

@dataclass    
class VolatileLeader:
    next_index: dict[int, int] = field(default_factory=list)
    match_index: dict[int, int] = field(default_factory=list)
