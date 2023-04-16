#!/data/data/com.termux/files/usr/bin/env python
import threading as th
import time
from os import environ, walk
from pathlib import Path

from asyncinotify import Event, Inotify, Mask, Watch

import config as v
import ldsv
import status as st
from findde import updateDEs
from fsmixin import FS_Mixin
from netup import netup
from opexec import clean, opExec
from status import onestatus, updatets

wdsi: dict[Watch, tuple[str, FS_Mixin]] = {}
sis: dict[v.NodeTag, list[str]] = {}
in1 = None
cel = None
cb1t = None
tr1 = 0
th1 = None
th2 = None


def wsetup():
    global wdsi, in1, v
    print("-wsetup")
    for si in v.srcs:
        try:
            p = v.src(si)
            pt = type(p)
            if p.is_dir() and not v.isbaddir(p) and isinstance(p, FS_Mixin):
                # TODO: not up to date
                for pth, dirs, files in walk(p, topdown=True):
                    pth = pt(pth)
                    v.proc_dirs(dirs, pt)
                    wa: Watch = in1.add_watch(
                        pth, Mask.MODIFY | Mask.CLOSE_WRITE | Mask.CREATE | Mask.DELETE
                    )
                    wdsi[wa] = si
        except Exception as e:
            print(e)
    print(len(wdsi), "watches")


def cb1():
    global th2, in1, v, sis
    print("-cb1-1")

    try:
        for ev in in1:
            # print("-cb1-2", ev)
            si = wdsi[ev.watch]
            # print("-cb1-3", si)
            p = ev.path
            if not ev.mask & Mask.ISDIR:
                # print("-cb1-5", fn)
                rfn = str(p.relative_to(v.src(si)))
                # print("-cb1-6", rfn)
                if si not in sis:
                    # print("-cb1-7")
                    sis[si] = []
                if rfn not in sis[si]:
                    print("-cb1-8", rfn)
                    sis[si].append(rfn)
                    if th2 is None:
                        th2 = th.Thread(target=proc_events)
                        th2.start()
    except Exception as e:
        print(e)
    print("-cb1-9")


def proc_events():
    global th2
    print("-proc_events-1")
    print(sis)
    for si in sis:
        print("-proc_events-2")
        p = v.src(si)
        sis[si], fl = [], sis[si]
        if len(fl):
            print("-proc_events-3: updateDEs", p, fl)
            updateDEs(p, fl)
    th2 = None


def rt2():
    print("-rt2-1")
    itc = 0
    while True:
        itc += 1
        print("-rt2-2")
        cl = clean()
        if cl:
            print("-rt2-3")
            print("no backups appear pending")
            rv1 = False
            break
        else:
            print("-rt2-4")
            print("backups appear pending")
            rv1 = opExec()
        print("-rt2-5")


def main():
    global cel, wdsi, in1, v, th1, th2
    v.initConfig()
    in1 = Inotify()
    wsetup()
    updatets(0)
    th1 = th.Thread(target=cb1)
    th1.start()
    rt2()
    ldsv.save_all()

if __name__ == "__main__":
    main()
