# Internal API
from .append_entries_req import append_entries_req
from .append_entries_req_resp import append_entries_req_resp
from data.append_entries_req import AppendEntriesReq
from data.append_entries_resp import AppendEntriesResp

from .vote_req import vote_req
from .vote_req_resp import vote_req_resp
from data.vote_req import VoteReq
from data.vote_resp import VoteResp

# External API
from .client_cmd_resp import client_cmd_resp

def send(self, in_msg, recipient_id):
    match self._handle:
        case self._leader:
            return self.append_entries_req(recipient_id)
        case self._candidate:
            return self.vote_req()
        case self._follower:
            match type(in_msg):
                case AppendEntriesReq():
                    return self.append_entries_req_resp(in_msg)
                case VoteReq():
                    return self.vote_req_resp(in_msg)
                
    return None
