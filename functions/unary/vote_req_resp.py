from data.vote_req import VoteReq
from data.vote_resp import VoteResp

def request_vote(self, request: VoteReq) -> VoteResp:
    vote_denied = VoteResp(
        term = self.persistent.current_term,
        vote_granted = False
    )
    
    if request.term < self.persistent.current_term:
        return vote_denied
    
    if (self.voted_for is None or self.voted_for == request.candidate_id) and \
       request.last_log_index == self.last_log_index and \
       request.last_log_term == self.last_log_term:
        self.voted_for = request.candidate_id
        
        vote_granted = VoteResp(
            term = request.term
            vote_granted = True
        )
        
        return vote_granted

    return vote_denied
