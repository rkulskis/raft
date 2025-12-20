from data.append_entries import RequestAppendEntries, RespondAppendEntries

def request_append_entries(self,
                           request: RequestAppendEntries) -> RespondAppendEntries:
    fail = AppendEntriesResponse(
        term = self.persistent.current_term,
        success = False
    )
    # 1. Deny request if sender has lower term than me
    if request.term < self.persistent.current_term:
        return fail

    # 2. Or if my log entry at prev_log_index doesn't match theirs
    if self.persistent.log[request.prev_log_index] != request.prev_log_term:
        return fail

    # We now know the request is valid.
    success = AppendEntriesResponse(
        term = self.persistent.current_term,
        success = True
    )

    # 3. Delete conflicting entries and all that follow
    new_entry_index = 0
    for (i, entry) in enumerate(request.entries, start=request.prev_log_index + 1):
        if len(self.persistent.log) <= i:
            break
        if self.persistent.log[i] != entry:
            log = log[:i]
            break
        new_entry_index += 1

    # 4. Append new entries not already in the log
    self.persistent.log.extend(request.entries[new_entry_index:])

    # 5. Adjust commit index based on leader commit and newest entry
    if request.leader_commit > self.volatile.commit_index:
        self.volatile.commit_index = min(request.leader_commit,
                                          len(self.persistent.log))

    return success
