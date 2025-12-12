def _start_election(self):
    self.persistent.current_term += 1
    self.persistent.voted_for = self.id
    self.election_timer.reset()

    # Send RequestVote RPC to all other peers. Count votes including self vote.
    votes = asyncio.gather(peer.request_vote() for peer in self.peers)
    votes_granted = sum(v.vote_granted for v in votes) + 1

    if 2 * votes_granted > len(self.peers):
        return self._tick_leader

    if self.received_append_entries:
        return self._tick_follower

    while not self.election_timer.elapsed():
        pass
    
    return self._start_election

_tick = _start_election
