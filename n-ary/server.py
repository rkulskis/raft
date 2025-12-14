from .state import Persistent, Volatile, VolatileLeader, StateMachine
from .follower import _tick as _tick_follower
from .candidate import _tick as _tick_candidate
from .leader import _tick as _tick_leader

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
        self.election_timer = None
        self.received_append_entries = False

        # Method to loop
        self._tick = self._tick_follower

    # Raft ticks like state machine
    _tick_follower = _tick_follower
    _tick_candidate = _tick_candidate
    _tick_leader = _tick_leader

    # For all servers, c.f. P4/18 "Rules for Servers" -> "All Servers"
    def _common_tick(self):
        if self.volatile.commit_index > self.volatile.last_applied:
            self.volatile.last_applied += 1
            self.state_machine.apply(
                self.persistent.log[self.volatile.last_applied]
            )
    
    def unmarshall(self, msg):
        if msg.term > self.persistent.current_term:
            self.persistent.current_term = msg.term
            self._tick = _tick_follower

        return msg
    # End all servers

    def run(self):
        while True:
            self._tick = self._tick()
            self._common_tick()
