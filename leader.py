def send_heartbeat(self):
    self.heartbeat_timer.reset()
    pass

def _tick(self):
    self.send_heartbeat()

    if self.client_cmd:
        self.persistent.log.append(self.client_cmd)
        self.client_cmd = None
        # Respond after entry applied to state machne

    for follower in self.peers:
        if self.last_log_index >= self.volatile_leader.next_index[follower.id]:
            while True:
                resp = follower.append_entries(
                    log[self.volatile_leader.next_index[follower.id]:]
                )
                if resp.ok:
                    self.volatile_leader.next_index[follower.id] = len(log)
                    self.volatile_leader.match_index[follower.id] = len(log)
                    break
                else:
                    self.volatile_leader.next_index[follower.id] -= 1

    # Commit up to (including) the largest index which a majority,
    # excluding me, matches and is part of the current term
    N_max = [sorted(self.volatile_leader.match_index)][
        int((len(self.peers) - 1) / 2)
    ]
    for N in range(self.volatile.commit_index + 1, N_max + 1):
        if self.persistent.log[N] == self.persistent.current_term:
            self.volatile.commit_index += 1
        else:
            break
