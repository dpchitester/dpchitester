import pickle

from sd import FS_Mixin


def prep_save():
    import config as v

    v.LDlls = {}
    v.LDlls_xt = {}
    v.LDhd = {}
    v.RDlls = {}
    v.RDlls_xt = {}
    v.RDhd = {}
    for si, pth in v.srcs.items():
        if isinstance(pth, FS_Mixin):
            if not pth.isremote:
                v.LDlls[si] = None  # pth.Dll
                v.LDlls_xt[si] = pth.Dll_xt
                v.LDlls_changed |= pth.Dll_changed
            else:
                v.RDlls[si] = pth.Dll
                v.RDlls_xt[si] = pth.Dll_xt
                v.RDlls_changed |= pth.Dll_changed
            if not pth.isremote:
                v.LDhd[si] = pth.SDh
            else:
                v.RDhd[si] = pth.SDh
    for di, pth in v.tgts.items():
        if isinstance(pth, FS_Mixin):
            if not pth.isremote:
                v.LDlls[di] = None  # pth.Dll
                v.LDlls_xt[di] = pth.Dll_xt
                v.LDlls_changed |= pth.Dll_changed
            else:
                v.RDlls[di] = pth.Dll
                v.RDlls_xt[di] = pth.Dll_xt
                v.RDlls_changed |= pth.Dll_changed
            if not pth.isremote:
                v.LDhd[di] = pth.SDh
            else:
                v.RDhd[di] = pth.SDh


def after_load():
    import config as v

    for si, pth in v.srcs.items():
        if not pth.isremote:
            if isinstance(pth, FS_Mixin):
                pth.Dll = None  # v.LDlls[si]
                pth.Dll_xt = v.LDlls_xt[si]
                pth.SDh = v.LDhd[si]
        else:
            if isinstance(pth, FS_Mixin):
                pth.Dll = v.RDlls[si]
                pth.Dlls_xt = v.RDlls_xt[si]
                pth.SDh = v.RDhd[si]
    for di, pth in v.tgts.items():
        if not pth.isremote:
            if isinstance(pth, FS_Mixin):
                pth.Dll = None  # v.LDlls[di]
                pth.Dll_xt = v.LDlls_xt[di]
                pth.SDh = v.LDhd[di]
        else:
            if isinstance(pth, FS_Mixin):
                pth.Dll = v.RDlls[di]
                pth.Dll_xt = v.RDlls_xt[di]
                pth.SDh = v.RDhd[di]


def loadldlls():
    import config as v

    try:
        with open(v.ldllsf, "rb") as fh:
            td = pickle.load(fh)
            v.LDlls = td["ldlls"]
            v.LDlls_xt = td["ldlls_xt"]
    except Exception as e:
        print("loadldlls failed", e)


def loadrdlls():
    import config as v

    try:
        with open(v.rdllsf, "rb") as fh:
            td = pickle.load(fh)
            v.RDlls = td["rdlls"]
            v.RDlls_xt = td["rdlls_xt"]
    except Exception as e:
        print("loadrdlls failed", e)


def saveldlls():
    import config as v

    # print('-saveldlls')
    if v.LDlls_changed:
        try:
            with open(v.ldllsf, "wb") as fh:
                td = {"ldlls": v.LDlls, "ldlls_xt": v.LDlls_xt}
                pickle.dump(td, fh)
                v.LDlls_changed = False
        except Exception as e:
            print("savedlls failed", e)


def saverdlls():
    import config as v

    # print('-saverdlls')
    if v.RDlls_changed:
        try:
            with open(v.rdllsf, "wb") as fh:
                td = {"rdlls": v.RDlls, "rdlls_xt": v.RDlls_xt}
                pickle.dump(td, fh)
                v.RDlls_changed = False
        except Exception as e:
            print("saverdlls failed", e)


def loadedges():
    import config as v

    try:
        with open(v.edgepf, "rb") as fh:
            v.eDep = pickle.load(fh)
    except Exception as e:
        print("loadedges failed", e)


def saveedges():
    import config as v

    # print("-saveedges")
    try:
        with open(v.edgepf, "wb") as fh:
            pickle.dump(v.eDep, fh)
    except Exception as e:
        print("saveedges failed", e)


def pstats():
    import config as v

    print("dl1_cs", v.dl1_cs)
    print("dl2_cs", v.dl2_cs)
    print("sfb", v.sfb)


def loadldh():
    import config as v

    try:
        with open(v.ldhpf, "rb") as fh:
            v.LDhd = pickle.load(fh)
    except Exception as e:
        print("loadldh failed", e)


def loadrdh():
    import config as v

    try:
        with open(v.rdhpf, "rb") as fh:
            v.RDhd = pickle.load(fh)
    except Exception as e:
        print("loadrdh failed", e)


def saveldh():
    import config as v

    try:
        with open(v.ldhpf, "wb") as fh:
            pickle.dump(v.LDhd, fh)
    except Exception as e:
        print("saveldh failed", e)


def saverdh():
    import config as v

    try:
        with open(v.rdhpf, "wb") as fh:
            pickle.dump(v.RDhd, fh)
    except Exception as e:
        print("saverdh failed", e)


def load_all():
    loadrdlls()
    loadldlls()
    loadedges()
    loadldh()
    loadrdh()
    try:
        after_load()
    except Exception as exc:
        print(exc)


def save_all():
    try:
        prep_save()
    except Exception as exc:
        print(exc)
    saverdlls()
    saveldlls()
    saveedges()
    saveldh()
    saverdh()
    pstats()
