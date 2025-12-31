def _leader(self):
    # Commit up to (including) the largest index which a majority,
    # excluding me, matches and is part of the current term
    N_max = sorted(self.volatile_leader.match_index.values())[self._majority() - 1]
    for N in range(self.volatile.commit_index + 1, N_max + 1):
        if self.persistent.log[N].term != self.persistent.current_term:
            break
        self.volatile.commit_index += 1
