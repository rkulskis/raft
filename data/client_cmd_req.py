from dataclasses import dataclass, field
import time

@dataclass
class ClientCmdReq:
    id: int = field(default_factory=time.time_ns) # monotonic increasing
    command: tuple[str, str] = ("", "")
    
