from data.client_cmd_resp import ClientCmdResp

def client_cmd_resp_recv(self, resp: ClientCmdResp):
    for i in range(self.commit_index + 1, len(self.persistent.log)):
        if resp.id >= self.persistent.log[i].id:
            print(f"Committed {self.persistent.log[i]}")
            self.commit_index += 1
        else:
            break
