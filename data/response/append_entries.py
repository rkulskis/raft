from dataclasses import dataclass

@dataclass    
class RespondAppendEntries:
    term: int
    success: bool
