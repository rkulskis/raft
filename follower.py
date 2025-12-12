def _respond_to_rpcs(self):
    pass

def _tick(self):
    self._respond_to_rpcs()
    
    if self.election_timer.elapsed() and not self.received_append_entries:
        return self._tick_candidate

    return _tick
