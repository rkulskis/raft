from data.client_cmd_req import ClientCmdReq

def client_cmd_req_recv(self, req: ClientCmdReq):
    if req.id <= self.persistent.log[-1].id:
        return
    
    new_entry = Entry(
        id=req.id,
        term=self.persistent.current_term,
        command=req.command
    )
    self.persistent.log.append(new_entry)
