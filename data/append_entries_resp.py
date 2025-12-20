from dataclasses import dataclass

@dataclass    
class AppendEntriesResp:
    term: int
    success: bool
