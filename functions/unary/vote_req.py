from data.vote_req import VoteReq

def vote_req(self) -> VoteReq:
    return VoteReq(
        term = self.persistent.current_term,
        candidate_id = self.id,
        prev_log_index = self.prev_log_index,
        last_log_term = self.last_log_term
    )
