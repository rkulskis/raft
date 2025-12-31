from data.vote_req import VoteReq
from data.vote_resp import VoteResp

def vote_req_resp(self, request: VoteReq) -> VoteResp:
    vote_denied = VoteResp(
        term = self.persistent.current_term,
        vote_granted = False
    )
    
    if request.term < self.persistent.current_term:
        return vote_denied

    # c.f. Raft paper P4/18, P8/18 penultimate paragraph
    if (self.voted_for == 0 or self.voted_for == request.candidate_id) and \
       (request.last_log_term > self.last_log_term or \
        (request.last_log_term == self.last_log_term and \
         request.prev_log_index >= self.prev_log_index)):
        self.voted_for = request.candidate_id
        
        vote_granted = VoteResp(
            term = request.term,
            vote_granted = True
        )
        
        return vote_granted

    return vote_denied
