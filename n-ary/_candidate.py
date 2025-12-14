def _start_election(self):
    self.persistent.current_term += 1
    self.persistent.voted_for = self.id
    self.election_timer.reset()

def _candidate(self):
    if self._is_majority(self._votes_granted):
        self.status = LEADER
        
    if self._received_append_entries:
        self.status = FOLLOWER
        
    if self.election_timer.elapsed():
        _start_election(self)
