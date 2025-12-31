from data.append_entries_req import AppendEntriesReq

def append_entries_req(self, recipient_id) -> AppendEntriesReq:
    prev_log_index = self.volatile_leader.next_index[recipient_id] - 1
    
    # need to handle heartbeat too
    entries = self.persistent.log[prev_log_index + 1:]
    
    request = AppendEntriesReq(
        term = self.persistent.current_term,
        leader_id = self.id,
        prev_log_index = self.prev_log_index,
        prev_log_term = self.persistent.log[prev_log_index].term,
        entries = entries,
        leader_commit = self.volatile.commit_index,
    )
    return request
