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
from data.client_cmd_req import ClientCmdReq
from .client_cmd_resp import client_cmd_resp
from .client_cmd_req import client_cmd_req

from state.raft_server_state import CLIENT_ID

def send(self, in_msg, recipient_id):
    if recipient_id == CLIENT_ID:
        if self._handle != self._leader:
            return None
        return self.client_cmd_resp()

    if self.id == CLIENT_ID:
        return self.client_cmd_req()
        
    match self._handle:
        case self._leader:
            print('Leader')
            return self.append_entries_req(recipient_id)
        
        case self._candidate:
            print('Candidate')
            return self.vote_req()
        
        case self._follower:
            print(f'Follower got {in_msg}')
            match in_msg:
                case AppendEntriesReq():
                    return self.append_entries_req_resp(in_msg)
                case VoteReq():
                    print('Follower responding')
                    return self.vote_req_resp(in_msg)
                
    return None
