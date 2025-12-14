from data.request_vote import RequestVote

@read_only
def request_vote(input) -> RequestVote:
    return RequestVote(
        term=self.persistent.current_term,
        candidate_id=self.id,
        last_log_index=self.last_log_index,
        last_log_term=self.last_log_term
    )
