from data.append_entries_resp import AppendEntriesResp
from .append_entries_resp_recv import append_entries_resp_recv

from data.vote_resp import VoteResp
from .vote_resp_recv import vote_resp_recv

def recv(self, msg, sender_id):
    if msg.term > self.persistent.current_term:
        self.persistent.current_term = msg.term
        self._handler = self._follower
        
    match type(msg):
        case AppendEntriesResp():
            append_entries_resp_recv(msg, sender_id)
        case VoteResp():
            vote_resp_recv(msg, sender_id)            
            
