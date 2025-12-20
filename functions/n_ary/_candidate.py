def _start_election(self):
    self.persistent.current_term += 1
    self.persistent.voted_for = self.id
    self.election_timeout.reset()

def _candidate(self):
    if self.election_timeout.elapsed():
        self._start_election()
    
    if self._votes_granted >= self._majority():
        self._handle = self._leader

    # Handled implicitly in recv.py
    # if self._received_append_entries:
        # convert to follower
