import time
import random

class Timer:
    def reset(self) -> None:
        self.start = time.perf_counter()
        rand_ofs = random.uniform(self.time_s * 0.5, self.time_s)
        self.end = self.start + rand_ofs
    
    def __init__(self, time_s: int):
        self.time_s = time_s
        self.reset()

    def elapsed(self) -> bool:
        return time.perf_counter() > self.end
