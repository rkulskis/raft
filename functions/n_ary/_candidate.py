def _candidate(self):
    def _start_election():
        self.persistent.current_term += 1
        self.persistent.voted_for = self.id
        self.election_timeout.reset()
    
    if self.election_timeout.elapsed():
        _start_election()
    
    if self._votes_granted >= self._majority():
        self._handle = self._leader

    # Handled implicitly in recv.py
    # if self._received_append_entries:
        # self._handle = self._follower
