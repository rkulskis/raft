# Internal API
from .append_entries_req import append_entries_req
from .vote_req import vote_req

# External API
from .client_cmd_resp import client_cmd_resp

def send(self, data, recipient_id):
