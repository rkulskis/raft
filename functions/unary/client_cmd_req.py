from data.client_cmd_req import ClientCmdReq

def client_cmd_req(self):
    if self.volatile.commit_index + 1 < len(self.persistent.log):
        command = self.persistent.log[self.volatile.commit_index + 1].command
        return ClientCmdReq(command=command)
    else:
        return None
