from data.request_vote import RequestVote, RespondVote

def request_vote(self, request: RequestVote) -> RespondVote:
    if request.term < self.persistent.current_term:
        return RespondVote(vote_granted=False)
    
    if (self.voted_for is None or self.voted_for == request.candidate_id) and \
       request.last_log_index == self.last_log_index and \
       request.last_log_term == self.last_log_term:
        return RespondVote(vote_granted=True)
    
    return RespondVote(vote_granted=False)
