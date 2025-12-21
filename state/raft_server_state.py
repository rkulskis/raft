from state.persistent import Persistent
from state.volatile import Volatile, VolatileLeader

from state.timer import Timer
from state.state_machine import StateMachine

from dataclasses import dataclass, field
from typing import Callable

@dataclass
class RaftServerState:
    id: int
    
    # From paper
    persistent: Persistent = field(default_factory=Persistent)
    volatile: Volatile = field(default_factory=Volatile)
    volatile_leader: VolatileLeader = field(default_factory=VolatileLeader)

    # Implicit from paper - initialized by calling process
    raft_cardinality: int = 0      # i.e. num servers in raft    
    
    # Other implicit from paper
    state_machine: StateMachine = field(default_factory=StateMachine)
    election_timeout: Timer = field(
        default_factory=lambda: Timer(time_s = 5 * 100e-3)
    )
    heartbeat_timers: dict[int, Timer] = field(
        default_factory=lambda: Timer(time_s = 100e-3)
    ) # leader has one for each peer (id)

    voted_for: int = 0
    _votes_granted: int = 0

    # Implementation-specific
    # unary
    # Generic
    from functions.unary.recv import recv
    from functions.unary.req_resp import req_resp
    from functions.unary.send import send
    
    # RPC-specific unary
    from functions.unary.append_entries_req import append_entries_req
    from functions.unary.append_entries_req_resp import append_entries_req_resp
    from functions.unary.append_entries_resp_recv import append_entries_resp_recv

    from functions.unary.client_cmd_req_recv import client_cmd_req_recv
    from functions.unary.client_cmd_resp import client_cmd_resp

    from functions.unary.vote_req import vote_req
    from functions.unary.vote_req_resp import vote_req_resp
    from functions.unary.vote_resp_recv import vote_resp_recv
    
    # n-ary
    from functions.n_ary._follower import _follower    
    from functions.n_ary._candidate import _candidate
    from functions.n_ary._leader import _leader
    from functions.n_ary.server import server
    
    _handle: Callable[[], None] = field(init=False)

    def __post_init__(self):
        # Bind the initial handler after instance is created
        self._handle = self._follower

    # Helpers
    def _majority(self):
        return int(self.raft_cardinality / 2) + 1

    def tick(self):
        self.server()
