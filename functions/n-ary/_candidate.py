def _start_election(self):
    self.persistent.current_term += 1
    self.persistent.voted_for = self.id
    self.election_timeout.reset()

def _candidate(self):
    if self.election_timeout.elapsed():
        _start_election(self)
    
    if self._is_majority(self._votes_granted):
        self.status = ServerStatus.LEADER
        
    if self._received_append_entries:
        self.status = ServerStatus.FOLLOWER
