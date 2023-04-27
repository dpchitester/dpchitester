from struct import pack, unpack

from xxhash import xxh64



def bhu(ho, it):
    from pathlib import Path, PosixPath
    from de import DE, FSe
    from sd import CS, SD, Ext3, Fat32
    match it:
        case bytes():
            ho.update(it)
        case int():
            ho.update(pack("i", it))
        case float():
            ho.update(pack("f", it))
        case str():
            ho.update(it.encode())
        case Path() | PosixPath() | SD() | Ext3() | Fat32() | CS():
            ho.update(bytes(it))
        case tuple() | set() | list():
            for it2 in it:
                bhu(ho, it2)
        case DE():
            ho.update(bytes(it.nm))
            ho.update(pack("i", it.i.sz))
            ho.update(pack("f", it.i.mt))
        case FSe():
            ho.update(pack("i", it.sz))
            ho.update(pack("f", it.mt))
        case _:
            print("key error", type(it), "??")


# flattened list blake2b with integer result
def blakeHash(it):
    ho = xxh64()
    bhu(ho, it)
    return ho.intdigest()
