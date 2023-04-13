import config as v
import ldsv
from edge import Edge, findEdge
from opbase import OpBase
from statushash import ldhset, rdhset


def changed_ops(T=None) -> list[OpBase]:
    rv: list[OpBase] = []
    for Op in v.opdep:
        di, si = Op.npl1
        if T is None or T == di:
            e: Edge = findEdge(di, si)
            if Op.ischanged(e):
                rv.append(Op)
    return rv


def stsupdate(Si, Dh):
    # print(Si, end=' ')
    print(Si, end=" ")
    # N1 = v.srcts[Si]
    for e in [e for e in v.eDep if e.si == Si]:
        e.rtset()
    ldhset(Si, Dh)


def rstsupdate(Di, Dh):
    # print(Si, end=' ')
    print(Di, end=" ")
    # N1 = v.srcts[Si]
    for e in [e for e in v.eDep if e.di == Di]:
        e.rrtset()
    rdhset(Di, Dh)


def onestatus(Si):
    # TODO: update as per src_statuses
    tr = v.lckers[Si]()
    if tr is not None:
        (Dh, changed) = tr
        if changed:
            stsupdate(Si, Dh)
            print()


def ronestatus(Di):
    # TODO: update as per tgt_statuses
    tr = v.rckers[Di]()
    if tr is not None:
        (Dh, changed) = tr
        if changed:
            rstsupdate(Di, Dh)
            print()


def src_statuses():
    SDl = []
    for Si in v.srcs:
        # print('calling lckers', Si)
        tr = v.lckers[Si]()
        if tr is not None:
            (Dh, changed) = tr
            if changed:
                SDl.append((Si, Dh))
    return SDl


def tgt_statuses():
    RDl = []
    excs = ["home", ".git"]
    for Di in v.tgts:
        if Di not in excs:
            tr = v.rckers[Di]()
            if tr is not None:
                (Dh, changed) = tr
                if changed:
                    RDl.append((Di, Dh))
    return RDl


def updatets(N):
    print("Status", N)
    Sl = src_statuses()
    if len(Sl):
        print("changed: ", end="")
        for Si, Dh in Sl:
            stsupdate(Si, Dh)
        print()


def rupdatets(N):
    print("RStatus", N)
    Dl = tgt_statuses()
    if len(Dl):
        print("rchanged: ", end="")
        for Di, Dh in Dl:
            rstsupdate(Di, Dh)
        print()


if __name__ == "__main__":
    updatets(1)
    rupdatets(1)
    print(changed_ops())
    ldsv.savefmd5h()
    ldsv.saveldlls()
    ldsv.saverdlls()
