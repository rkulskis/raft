from data.append_entries import RequestAppendEntries, RespondAppendEntries

def request_append_entries(self, req: RequestAppendEntries) -> RespondAppendEntries:
    # 1. Deny request if sender has lower term than me
    if req.term < self.persistent.current_term:
        return AppendEntriesResp(ok=False)

    # 2. Or if my log entry at prev_log_index doesn't match theirs
    if self.persistent.log[req.prev_log_index] != req.prev_log_term:
        return AppendEntriesResp(ok=False)

    # We now know the request is valid.

    # 3. Delete conflicting entries and all that follow
    new_entry_index = 0
    for (i, entry) in enumerate(req.entries, start=req.prev_log_index + 1):
        if len(self.persistent.log) <= i:
            break
        if self.persistent.log[i] != entry:
            log = log[:i]
            break
        new_entry_index += 1

    # 4. Append new entries not already in the log
    self.persistent.log.extend(req.entries[new_entry_index:])

    # 5. Adjust commit index based on leader commit and newest entry
    if req.leader_commit > self.volatile.commit_index:
        self.volatile.commit_index = min(req.leader_commit,
                                          len(self.persistent.log))

    return AppendEntriesResp(ok=True)
