from data.append_entries import RequestAppendEntries

@read_only
def request_append_entries(self, recipient_id) -> RequestAppendEntries:
    prev_log_index = self.volatile_leader.next_index[recipient_id] - 1
    # need to handle heartbeat too
    entries = self.persistent.log[prev_log_index + 1:]
    request = AppendEntriesReq(
        term = self.persistent.current_term,
        leader_id = self.persistent.id,
        prev_log_index = prev_log_index,
        prev_log_term = self.persistent.log[prev_log_index].term,
        entries = entries
        leader_commit = self.volatile.commit_index
    )
    return request
