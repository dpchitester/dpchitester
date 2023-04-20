import datetime as dt

import asyncrun as ar
from netup import netup
from opbase import OpBase


class SFc:
    sc = 0
    fc = 0

    def __init__(self):
        pass

    def value(self):
        return (self.sc, self.fc)


def ts2st(ts):
    import config as v

    t2 = v.ts_trunc2ms(ts)
    t2 = dt.datetime.fromtimestamp(t2, tz=dt.timezone.utc)
    t2 = t2.isoformat()[:-6]
    return t2


def ftouch(di, si, td, lf, sfc):
    if netup():
        nt = ts2st(lf.i.mt)
        cmd = (
            'rclone touch "'
            + str(td / lf.nm)
            + '" --timestamp "'
            + nt
            + '" --progress --no-create'
        )
        # cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
        print(cmd)
        rc = ar.run2(cmd)
        if rc == 0:
            sfc.sc += 1
            return True
        else:
            sfc.fc += 1
            print(ar.txt)
    return False


def fsync(di, si, sd, td, sfc):
    if netup():
        # print('copy', sd, td)
        cmd = (
            'rclone copy "'
            + str(sd.parent)
            + '" "'
            + str(td.parent)
            + '" --include "'
            + str(td.name)
            + '" --progress --no-traverse'
        )
        # cmd += ' --exclude ".git/**" --exclude "__pycache__/**"'
        print(cmd)
        rc = ar.run2(cmd)
        if rc == 0:
            sfc.sc += 1
            return True
        else:
            sfc.fc += 1
            print(ar.txt)
    return False


def fsyncl(di, si, sd, td, fl, sfc):
    cmd = 'rclone copy "'
    cmd += str(sd) + '" "'
    cmd += str(td) + '" '
    for fn in fl:
        cmd += '--include "' + str(fn.nm) + '" '
    cmd += "--progress --no-traverse"
    # cmd += '--exclude "**/.git/**/*" '
    # cmd += '--exclude "**/__pycache__/**/*" '
    # cmd += '--exclude "**/node_modules/**/*" '
    # cmd += '--log-file="rclone.log" '
    # cmd += "--use-json-log"
    if netup():
        # print("copy", sd, td, list(map(lambda de: str(de.nm), fl)))
        print(cmd)
        rc = ar.run2(cmd)
        if rc == 0:
            sfc.sc += len(fl)
            return True
        else:
            sfc.fc += 1
            print(ar.txt)
    return False


def fdel(di, si, sd, td, sfc):
    if netup():
        cmd = 'rclone delete "'
        cmd += str(td)
        cmd += '" --progress'
        print(cmd)
        rc = ar.run2(cmd)
        if rc == 0:
            sfc.sc += 1
            return True
        else:
            sfc.fc += 1
            print(ar.txt)
    return False


def fdell(di, si, td, fl, sfc):
    cmd = 'rclone delete "'
    cmd += str(td) + '" '
    for fn in fl:
        cmd += '--include "' + str(fn.nm) + '" '
    cmd += "--progress"
    # cmd += '--log-file="rclone.log" '
    # cmd += "--use-json-log"
    if netup():
        # print("delete", td, list(map(lambda de: str(de.nm), fl)))
        print(cmd)
        rc = ar.run2(cmd)
        if rc == 0:
            sfc.sc += 1
            return True
        else:
            sfc.fc += 1
            print(ar.txt)
    return False


class BVars:
    def __init__(self, di, si, sfc):
        import config as v

        self.si = si
        self.di = di
        self.sd = v.src(si)
        self.td = v.tgt(di)
        self.src_dls = None
        self.dst_dls = None
        self.f2d = None
        self.f2c = None
        self.f2t = None
        self.sfc = sfc
        self.ac2 = 0

    def init2(self):
        import config as v
        from dirlist import dllcmp

        self.src_dls = self.sd.Dlld()
        if self.src_dls is None:
            self.sfc.fc += 1
        self.dst_dls = self.td.Dlld()
        if self.dst_dls is None:
            self.sfc.fc += 1
        if self.src_dls is not None and self.dst_dls is not None:
            # v.proc_DEs(self.src_dls)
            self.f2d, self.f2c = dllcmp(self.dst_dls, self.src_dls)
        self.f2t = set()

    def skip_matching(self):
        # handle slip through mismatched on times or more recent
        from findde import updateDEs

        for rf in self.f2d.copy():
            for lf in self.f2c.copy():
                # TODO: use Path
                if rf.nm == lf.nm:  # names match
                    if rf.i.sz == lf.i.sz and rf.i.mt == lf.i.mt:  # sz,mt match
                        self.f2d.remove(rf)
                        self.f2c.remove(lf)
                    elif rf.i.sz == lf.i.sz:
                        print(rf.i.mt, lf.i.mt, rf.i.mt - lf.i.mt)
                        if rf.i.mt > lf.i.mt:
                            if rf.i.mt - lf.i.mt > 0.0001:
                                self.f2t.add(lf)
                            # if rf.i.mt-lf.i.mt<-0.0001:
                            # if ftouch(self.di, self.si, self.sd, rf, self.sfc):
                            # updateDEs(self.sd, [str(de.nm) for de in [rf]])

    def do_touching(self):
        # TODO: use Path
        from findde import updateDEs
        from status import onestatus

        cfpl = self.f2t.copy()
        if len(cfpl) == 0:
            return
        # print(cfp)
        for lf in cfpl:
            if ftouch(self.di, self.si, self.td, lf, self.sfc):
                self.ac2 += 1
                try:
                    self.f2t.remove(lf)
                except KeyError:
                    pass
        updateDEs(self.td, [str(de.nm) for de in cfpl])

    def do_copying(self):
        # TODO: use Path
        from status import onestatus

        cfpl = self.f2c.copy()
        if len(cfpl) == 0:
            return
        # print(cfp)
        if fsyncl(self.di, self.si, self.sd, self.td, cfpl, self.sfc):
            from findde import updateDEs

            for lf in cfpl:
                self.ac2 += 1
                try:
                    self.f2c.remove(lf)
                except KeyError:
                    pass
                for rf in self.f2d.copy():
                    if str(rf.nm) == str(lf.nm):
                        try:
                            self.f2d.remove(rf)
                        except KeyError:
                            pass
            updateDEs(self.td, [str(de.nm) for de in cfpl])

    def do_deletions(self):
        from findde import updateDEs
        from status import onestatus

        cfpl = self.f2d.copy()
        if fdell(self.di, self.si, self.td, cfpl, self.sfc):
            for rf in cfpl:  # do deletions
                self.ac2 += 1
                try:
                    self.f2d.remove(rf)
                except KeyError:
                    pass
        updateDEs(self.td, [str(de.nm) for de in cfpl])
    def list_deletions(self):
        from findde import updateDEs
        from status import onestatus

        cfpl = self.f2d.copy()
        print('potential deletions', cfpl)


class CSCopy(OpBase):
    from edge import Edge, findEdge

    def __init__(self, npl1, npl2, opts={}):
        super(CSCopy, self).__init__(npl1, npl2, opts)
        self.sfc = SFc()

    def ischanged(self, e: Edge):
        return e.chk_ct() or e.rchk_ct()

    def __call__(self):
        import config as v
        from edge import Edge, findEdge
        from status import onestatus

        di, si = self.npl1
        print("CSCopy", si + "->" + di)
        if not netup():
            self.sfc.fc += 1
            return self.sfc.value()
        e: Edge = findEdge(di, si)
        if e.chk_ct():
            bv = BVars(di, si, self.sfc)
            bv.init2()
            if bv.sfc.fc == 0:
                print("raw", len(bv.f2d), "todelete", len(bv.f2c), "tocopy")
                bv.skip_matching()
                print("skip", len(bv.f2d), "todelete", len(bv.f2c), "tocopy")
            if bv.sfc.fc == 0:
                bv.do_copying()
            if bv.sfc.fc == 0:
                if "listdeletions" in self.opts and self.opts["listdeletions"] and len(bv.f2d):
                    bv.list_deletions()
            if bv.sfc.fc == 0:
                if "delete" in self.opts and self.opts["delete"] and len(bv.f2d):
                    bv.do_deletions()
            if bv.sfc.fc == 0:
                bv.do_touching()
            if bv.ac2:
                pass
        if self.sfc.fc == 0:
            e.clr()
            e.rclr()
        if self.sfc.sc > 0:
            if di in v.srcs:
                onestatus(di)
        return self.sfc.value()
