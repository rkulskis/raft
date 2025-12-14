from ._client_cmd import _client_cmd
from ._request_append_entries import _request_append_entries
from ._request_vote import _request_vote
from ._respond_append_entries import _respond_append_entries
from ._respond_vote import _respond_vote

def server(self, data, recipient_id):
    if msg.term > self.persistent.current_term:
        self.persistent.current_term = msg.term
        self.status = ServerStatus.FOLLOWER
        
    match type(data):
        case ClientCmd:
            self._client_cmd(data)
        case RequestAppendEntries:
            self._request_append_entries(data, recipient_id)
        case RequestVote:
            self._request_vote(data)
        case RespondAppendEntries:
            self._respond_append_entries(data, recipient_id)
        case RespondVote:
            self._respond_vote(data)           
