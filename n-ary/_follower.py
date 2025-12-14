def _follower(self):
    if self.election_timer.elapsed() and \
       not (self._received_append_entries or self.voted_for):
        self.status = CANDIDATE
