from data.entry import Entry

import sys
import time

def client(self):
    if (line := sys.stdin.readline().strip()):
        print("client")        
        parts = line.split()
        if len(parts) != 2:
            print("Expected exactly two values")
            return

        key, val = parts

    if time.time_ns() > self.persistent.log[-1].id + 1e9:
        command = ("bruh", f"{time.time_ns()}")
        print(f"Adding {command}")
        self.persistent.log.append(Entry(command=command))
