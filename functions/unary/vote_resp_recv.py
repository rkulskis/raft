from data.vote_resp import VoteResp

def vote_resp_recv(self, response: VoteResp) -> None:
    if response.vote_granted:
        self._votes_granted += 1
