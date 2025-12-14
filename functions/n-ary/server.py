from state.persistent import Persistent
from state.volatile import Volatile, VolatileLeader

from ._follower import _follower
from ._candidate import _candidate
from ._leader import _leader

from enum import Enum

class ServerStatus(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3
    
class Server:
    def __init__(self, id):
        self.id = id
        self.peers = []

        # From paper
        self.persistent = Persistent()        
        self.volatile = Volatile()
        self.volatile_leader = VolatileLeader()
        
        self.state_machine = StateMachine()

        # Flags
        self.status = ServerStatus.FOLLOWER
        self.election_timer = None
        self.received_append_entries = False

    _follower = _follower
    _candidate = _candidate
    _leader = _leader

    n_ary = {
        ServerStatus.FOLLOWER: _follower,
        ServerStatus.CANDIDATE: _candidate,
        ServerStatus.LEADER: _leader,
    }

    # For all servers, c.f. P4/18 "Rules for Servers" -> "All Servers"
    def run(self, inputs, subscribers):
        _prior_status = self.status
        self.n_ary[self.status]
        
        if _prior_status != self.status: # conversion
            self.n_ary[self.status]
        
        if self.volatile.commit_index > self.volatile.last_applied:
            self.volatile.last_applied += 1
            self.state_machine.apply(
                self.persistent.log[self.volatile.last_applied]
            )
        return msg
