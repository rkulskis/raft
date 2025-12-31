from data.client_cmd_resp import ClientCmdResp

def client_cmd_resp(self):
    if self.volatile.commit_index == len(self.persistent.log):
        return ClientCmdResp(id=self.persistent.log[-1].id)
