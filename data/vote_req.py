from dataclasses import dataclass

@dataclass
class VoteReq:
    term: int
    candidate_id: int
    prev_log_index: int
    last_log_term: int
