from data.request_vote import RespondVote

def respond_vote(self, response: RespondVote) -> None:
    if response.vote_granted:
        self._votes_granted += 1
