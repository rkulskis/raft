def _follower(self):
    # If received input from valid leader, e.g. append_entries,
    # election timeout resets; this is handled at the recv.py layer
    if self.election_timeout.elapsed() and self.voted_for == 0:
        self._handle = self._candidate
