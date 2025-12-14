from multiprocessing import shared_memory

class FourSlotShared:
    latest: int
    reading: int
    slot: int[2][2]

class FourSlot:
    shm: SharedMemory

def fourslot_write(data: int, _buf: FourSlot) -> int:
    buf = _buf.buf
    
    pair = buf.latest
    index = buf.slot[pair]

    buf.slot[pair][index] = data
    buf.slot[pair] = index
    buf.latest = pair

    return 0

def fourslot_read(_buf: FourSlot) -> int:
    buf = _buf.buf
    
    pair = buf.latest
    buf.reading = latest
    index = buf.slot[pair]

    return buf.slot[pair][index]

def new_fourslot(create=False, name: str) -> FourSlot:
    return shared_memory.SharedMemory(create=create, size=FourSlotShared)
    
def del_fourslot(unlink=False, buf: FourSlot):
    buf.close()
    buf.unlink(unlink=unlink)
    
