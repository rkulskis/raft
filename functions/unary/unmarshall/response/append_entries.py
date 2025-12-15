from data.append_entries import RespondAppendEntries

def respond_append_entries(self,
                           response: RespondAppendEntries,
                           input_id: int) -> None:
    if response.success:
        self.volatile_leader.next_index[input_id] = len(log)
        self.volatile_leader.match_index[input_id] = len(log)
    else:
        self.volatile_leader.next_index[input_id] -= 1
