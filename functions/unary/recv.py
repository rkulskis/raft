def recv(self, data, recipient_id):
    if msg.term > self.persistent.current_term:
        self.persistent.current_term = msg.term
        self.status = ServerStatus.FOLLOWER
