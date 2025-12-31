from data.append_entries_resp import AppendEntriesResp

def append_entries_resp_recv(self,
                             response: AppendEntriesResp,
                             input_id: int) -> None:
    if response.success:
        self.volatile_leader.match_index[input_id] = \
            self.volatile_leader.next_index[input_id] = \
                len(self.persistent.log) - 1
    else:
        self.volatile_leader.next_index[input_id] -= 1
