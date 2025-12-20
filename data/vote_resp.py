from dataclasses import dataclass

@dataclass    
class VoteResp:
    term: int
    vote_granted: bool
