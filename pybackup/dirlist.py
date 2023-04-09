import asyncio
import datetime
import json
import time
from bisect import bisect_left
from fnmatch import fnmatch
from os import walk
from pathlib import Path

import asyncrun as ar
import config as v
from bhash import blakeHash
from fmd5h import fmd5f

rto1 = 60 * 1
rto2 = 60 * 1


def getfl(p):
    # print(str(p))
    fl = []
    try:
        if p.is_file():
            fl.append(p)
            return fl
        for pth, dirs, files in walk(p, topdown=True):
            if ".git" in pth:
                dirs = []
                break
            if ".git" in dirs:
                dirs.remove(".git")
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            for f in files:
                fl.append(Path(pth, f))
        return fl
    except Exception as e:
        print(e)
        return None


def getDL(p):
    # print(str(p))
    fl = []
    try:
        for pth, dirs, files in walk(p, topdown=True):
            if ".git" in pth:
                dirs = []
                break
            if ".git" in dirs:
                dirs.remove(".git")
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            for d in dirs.copy():
                fl.append(Path(pth, d))
                dirs.remove(d)
            break
        return fl
    except Exception as e:
        print("getDL", e)
        return None


def getdll0():
    v.dl0_cs += 1
    td = v.ppre("gd")
    # print('getdll0',td)
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --hash'
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it):
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-1] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            if "Hashes" in it:
                it4 = bytes.fromhex(it["Hashes"]["md5"])
            else:
                it4 = bytes()
            return v.DE(it1, it2, it3, it4)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        print(len(st), "de's")
        return st
    return None


def sepdlls(dlls):
    print("-sepdlls")
    for di in v.tgts:
        if di.startswith("gd_"):
            v.RDlls[di] = []
            v.RDlls_xt[di] = time.time()
            v.RDlls_changed = True
            rd = v.tgt(di).relative_to(v.ppre("gd"))
            tds = str(rd) + "/"
            i = bisect_left(dlls, tds, key=lambda de: de.nm)
            # print(tds, i)
            if i == len(dlls):
                continue
            de = dlls[i]
            if not fnmatch(de.nm, tds + "*"):
                print("error")
                print(rd, tds, i, de.nm)
                # TODO: apply panic procedure
                continue
            while fnmatch(de.nm, tds + "*"):
                de2 = v.DE(de.nm, de.sz, de.mt, de.md5)
                # TODO: use Path
                de2.nm = de2.nm.relative_to(rd)
                # print(de2[0])
                # if de2 in csdlls[di]:
                # csdlls[di].remove(de2)
                v.RDlls[di].append(de2)
                i += 1
                if i == len(dlls):
                    break
                de = dlls[i]
    print(len(v.RDlls), "rdlls")


def getdll1(di):
    v.dl1_cs += 1
    td = v.tgt(di)
    # print('getdll1', di, str(td))
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --hash --fast-list'
    # print(cmd)
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it):
            # TODO: use Path
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-1] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            if "Hashes" in it:
                it4 = bytes.fromhex(it["Hashes"]["md5"])
            else:
                it4 = bytes()
            return v.DE(it1, it2, it3, it4)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        return st
    if rc == 3:
        return []
    return None


def getdll2(si):
    v.dl2_cs += 1
    td = v.pdir(si)
    # print('getdll2', si, str(td))
    cmd = 'rclone lsjson "' + str(td) + '" --recursive --files-only --hash --fast-list'
    if not td.is_file():
        cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
    # print(cmd)
    rc = ar.run1(cmd)
    if rc == 0:
        l1 = json.loads(ar.txt)

        def es(it):
            # TODO: use Path
            it1 = Path(it["Path"])
            it2 = it["Size"]
            it3 = it["ModTime"][:-7] + "-00:00"
            it3 = datetime.datetime.fromisoformat(it3).timestamp()
            if "Hashes" in it:
                it4 = bytes.fromhex(it["Hashes"]["md5"])
            else:
                it4 = bytes()
            return v.DE(it1, it2, it3, it4)

        st = list(map(es, l1))
        st.sort(key=lambda de: de.nm)
        return st
    if rc == 3:
        return []
    return None


def getdll3(si):
    v.dl3_cs += 1
    sd = v.srcDir(si)
    # print('getdll3', si, str(sd))
    l1 = getfl(sd)

    def es(it):
        # TODO: use Path
        it1 = it.relative_to(sd)
        fs = it.stat()
        it2 = fs.st_size
        it3 = fs.st_mtime_ns
        it3 = v.trunc2ms(it3)
        it4 = fmd5f(it, it2, it3)
        return v.DE(it1, it2, it3, it4)

    st = list(map(es, l1))
    st.sort(key=lambda de: de.nm)
    return st


def getrdlls():
    t1 = time.time()
    rv = getdll0()
    if rv is not None:
        t2 = time.time()
        sepdlls(rv)
        t3 = time.time()
        print(round(t2 - t1, 3), round(t3 - t2, 3))


def lDlld(si):
    # print('-ldlld', si)
    if si not in v.LDlls or v.LDlls_xt[si] + rto1 <= time.time():
        print("obtaining", si, "ldll...", end='')
        rv = getdll3(si)
        if rv is not None:
            print("done.")
            v.LDlls[si] = rv
            v.LDlls_xt[si] = time.time()
            v.LDlls_changed = True
        else:
            print("failed.")
    return v.LDlls[si]


def rDlld(di):
    # print('-rdlld', di)
    if di not in v.RDlls or v.RDlls_xt[di] + rto2 <= time.time():
        print("obtaining", di, "rdll...", end='')
        rv = getdll1(di)
        if rv is not None:
            print("done.")
            v.RDlls[di] = rv
            v.RDlls_xt[di] = time.time()
            v.RDlls_changed = True
        else:
            print("failed.")
    return v.RDlls[di]


def dllcmp(do, dn):
    dns = set(dn)
    dos = set(do)
    tocopy = dns - dos
    todelete = dos - dns
    return (todelete, tocopy)


def getRemoteDE(di, sf: Path):
    cmd = 'rclone lsjson "' + str(sf) + '" --hash'
    rc = ar.run1(cmd)
    if rc == 0:
        rd = sf.relative_to(v.tgt(di)).parent
        it = json.loads(ar.txt)[0]
        it1 = rd / it["Path"]
        it2 = it["Size"]
        it3 = it["ModTime"][:-1] + "-00:00"
        it3 = datetime.datetime.fromisoformat(it3).timestamp()
        if "Hashes" in it:
            it4 = bytes.fromhex(it["Hashes"]["md5"])
        else:
            it4 = bytes()
        nde = v.DE(it1, it2, it3, it4)
        print("new nde:", nde.nm, nde.sz, nde.mt)
        return nde

def findLDE(si, sd, dl):
    ld = sd.relative_to(v.pdir(si))
    i = bisect_left(dl, ld, key=lambda de: de.nm)
    return i


def findRDE(di, td, dl):
    rd = td.relative_to(v.tgt(di))
    i = bisect_left(dl, rd, key=lambda de: de.nm)
    return i
