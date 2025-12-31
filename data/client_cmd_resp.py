from dataclasses import dataclass, field
import time

@dataclass
class ClientCmdResp:            # ack
    id: int
