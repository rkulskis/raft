from ._client_cmd import _client_cmd
from ._request_append_entries import _request_append_entries
from ._request_vote import _request_vote

def server(self, data, recipient_id):
    match type(data):
        case ClientCmd:
            self._client_cmd(data)
        case RequestAppendEntries:
            self._request_append_entries(data, recipient_id)
        case RequestVote:
            self._request_vote(data)
            
