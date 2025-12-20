from dataclasses import dataclass

@dataclass    
class RespondVote:
    term: int
    vote_granted: bool
