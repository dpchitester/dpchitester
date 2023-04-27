import datetime
import time
from pathlib import Path, PosixPath

import asyncrun as ar
import ldsv as ls
from de import DE, FSe

# from snoop import pp, snoop


icl = 1
rto1 = 60 * 60


class SD(PosixPath):
    def __new__(cls, *args, **kwargs):
        return super(SD, cls).__new__(cls, *args)

    def __init__(self, *args, **kwargs):
        super(SD, self).__init__(*args, **kwargs)

    def sdh_f(self, dh=None):
        odh = self.SDh
        if dh is not None:
            self.SDh = dh
        return odh

    def sdhset(self, Dh=None):
        if Dh is None:
            Dh = self.sdh_d()
        if Dh is not None:
            self.sdh_f(Dh)

    def sdhck(self):
        Dh1 = self.sdh_f()
        Dh2 = self.sdh_d()
        if Dh2 is not None:
            return (Dh2, Dh1 != Dh2)
        return (None, False)


class Local_Mixin:
    def __init__(self, *args, **kwargs):
        super(Local_Mixin, self).__init__()

    @property
    def isremote(self):
        return False

    @property
    def Dll(self):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in v.LDlls:
                    return v.LDlls[self.tag]
        return None

    @Dll.setter
    def Dll(self, val):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                v.LDlls[self.tag] = val
                ls.sev.put("ldlls")

    @property
    def Dlls_xt(self):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in v.LDlls_xt:
                    return v.LDlls_xt[self.tag]
        return 0

    @Dlls_xt.setter
    def Dlls_xt(self, val):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                v.LDlls_xt[self.tag] = val
                ls.sev.put("ldlls")

    @property
    def SDh(self):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in v.LDhd:
                    return v.LDhd[self.tag]
        return 0

    @SDh.setter
    def SDh(self, val):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                v.LDhd[self.tag] = val
                ls.sev.put("ldhd")


class Remote_Mixin:
    def __init__(self, *args, **kwargs):
        super(Remote_Mixin, self).__init__()

    @property
    def isremote(self):
        return True

    @property
    def Dll(self):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in v.RDlls:
                    return v.RDlls[self.tag]
        return None

    @Dll.setter
    def Dll(self, val):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                v.RDlls[self.tag] = val
                ls.sev.put("rdlls")

    @property
    def Dlls_xt(self):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in v.RDlls_xt:
                    return v.RDlls_xt[self.tag]
        return 0

    @Dlls_xt.setter
    def Dlls_xt(self, val):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                v.RDlls_xt[self.tag] = val
                ls.sev.put("rdlls")

    @property
    def SDh(self):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                if self.tag in v.RDhd:
                    return v.RDhd[self.tag]
        return 0

    @SDh.setter
    def SDh(self, val):
        import config as v

        if hasattr(self, "tag"):
            with ls.dl:
                v.RDhd[self.tag] = val
                ls.sev.put("rdhd")


class FS_Mixin(SD):
    def __init__(self, *args, **kwargs):
        super(FS_Mixin, self).__init__(*args, **kwargs)

    def sdh_d(self):
        from bhash import blakeHash

        with ls.dl:
            Si_dl = self.Dlld()
        if Si_dl is not None:
            return blakeHash(Si_dl)
        return None

    def Dlld(self):
        from filelist import FileList

        # print('-ldlld', si)
        if self.isremote:
            ch = "r"
        else:
            ch = "l"
        if self.Dll is None or (self.isremote and self.Dlls_xt + rto1 <= time.time()):
            print("sucking/scanning for", self.tag, ch + "dll...", end="")
            rv = FileList(self).getdll()
            # rv = self.getdll()
            if rv is not None:
                print("done.")
                self.Dll = rv
                self.Dlls_xt = time.time()
            else:
                print("failed.")
                pass
        else:
            print("fetched", self.tag, ch + "dll from cache.")
            pass
        return self.Dll


class CFS_Mixin(FS_Mixin, Remote_Mixin):
    def __init__(self, *args, **kwargs):
        super(CFS_Mixin, self).__init__(*args, **kwargs)


class PFS_Mixin(FS_Mixin, Local_Mixin):
    def __init__(self, *args, **kwargs):
        super(PFS_Mixin, self).__init__(*args, **kwargs)


class Ext3(PFS_Mixin):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(Ext3, self).__init__(*args, **kwargs)


class Fat32(PFS_Mixin):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(Fat32, self).__init__(*args, **kwargs)


class CS(CFS_Mixin):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super(CS, self).__init__(*args, **kwargs)
