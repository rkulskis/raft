# For all servers, c.f. P4/18 "Rules for Servers" -> "All Servers"
def server(self):
    _prior_handle = self._handle
    self._handle()

    converted = (_prior_handle != self._handle)

    if converted:
        self._handle()

    # c.f. P4/18 "All Servers"; note: do incrementally to balance
    # I/O load across server loops
    if self.volatile.commit_index > self.volatile.last_applied:
        self.volatile.last_applied += 1
        self.state_machine.apply(
            self.persistent.log[self.volatile.last_applied]
        )
