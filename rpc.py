# ******************** Request Vote ********************
@dataclass
class RequestVoteReq:
    term: int
    candidate_id: int
    last_log_index: int
    last_log_term: int

@dataclass    
class RequestVoteResp:
    vote_granted: bool

def request_vote_req(req: RequestVoteReq):
    
# ******************* Append Entries *******************
@dataclass
class AppendEntriesReq:
    term: int
    leader_id: int
    prev_log_index: int
    prev_log_term: int
    entries: list[int]
    leader_commit: int

@dataclass    
class AppendEntriesResp:
    ok: bool

# These functions return the message datatype based on state

def append_entries_req(self, recipient_id, is_heartbeat=False) -> AppendEntriesReq:
    prev_log_index = self.volatile_leader.next_index[recipient_id] - 1
    entries = self.persistent.log[prev_log_index + 1:] if not is_heartbeat else []
    req = AppendEntriesReq(
        term = self.persistent.current_term,
        leader_id = self.persistent.id,
        prev_log_index = prev_log_index,
        prev_log_term = self.persistent.log[prev_log_index].term,
        entries = entries
        leader_commit = self.volatile.commit_index
    )
    return req

def append_entries_resp(self, req: AppendEntriesReq) -> AppendEntriesResp:
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
