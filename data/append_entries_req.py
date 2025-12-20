from dataclasses import dataclass

@dataclass
class AppendEntriesReq:
    term: int
    leader_id: int
    prev_log_index: int
    prev_log_term: int
    entries: list[int]
    leader_commit: int
