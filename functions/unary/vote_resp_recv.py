from data.vote_resp import VoteResp

def respond_vote(self, response: VoteResp) -> None:
    if response.vote_granted:
        self._votes_granted += 1
