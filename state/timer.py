import time

class Timer:
    def __init__(self, time_s: int):
        self.time_s = time_s
        self.start = time.time()
        self.end = self.start + self.time_s

    def reset(self) -> None:
        self.start = time.time()
        self.end = self.start + self.time_s

    def elapsed(self) -> bool:
        return time.time() > self.end
