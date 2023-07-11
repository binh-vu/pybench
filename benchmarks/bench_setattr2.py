from __future__ import annotations
from dataclasses import dataclass
import os
from typing import Iterator, List, Literal
from pybench.base import BenchSetup

from pybench.helper import get_module


class SetAttrBaseCls1:
    __slots__ = []

    def __init__(self, *args, **kwargs):
        for name, arg in zip(self.__slots__, args):
            setattr(self, name, arg)
        for name, arg in kwargs.items():
            setattr(self, name, arg)


class SetAttrBaseCls2:
    __slots__ = []

    def __init__(self, *args):
        for name, arg in zip(self.__slots__, args):
            setattr(self, name, arg)


class SetAttrBaseCls3:
    __slots__ = []

    def __init__(self, **kwargs):
        for name, arg in kwargs.items():
            setattr(self, name, arg)


# fmt: off
attrs = ['pwLF', 'pmYG', 'ncdv', 'umNRVn', 'Adyej', 'qrwxo', 'SltAK', 'qDv', 'pwLPZm', 'tVTRM', 'Edft', 'XaHNFj', 'SvoyjOb', 'FJzohYF', 'adPFnLb', 'rjX', 'FcQI', 'lwSINx', 'SZoDZaC', 'GuUbA']

class SetAttrCls1(SetAttrBaseCls1):
    __slots__ = attrs

class SetAttrCls2(SetAttrBaseCls2):
    __slots__ = attrs

class SetAttrCls3(SetAttrBaseCls3):
    __slots__ = attrs

class SetAttrCls4(SetAttrBaseCls1):
    __slots__ = attrs

    def __init__(self, pwLF, pmYG, ncdv, umNRVn, Adyej, qrwxo, SltAK, qDv, pwLPZm, tVTRM, Edft, XaHNFj, SvoyjOb, FJzohYF, adPFnLb, rjX, FcQI, lwSINx, SZoDZaC, GuUbA):
        self.pwLF = pwLF
        self.pmYG = pmYG
        self.ncdv = ncdv
        self.umNRVn = umNRVn
        self.Adyej = Adyej
        self.qrwxo = qrwxo
        self.SltAK = SltAK
        self.qDv = qDv
        self.pwLPZm = pwLPZm
        self.tVTRM = tVTRM
        self.Edft = Edft
        self.XaHNFj = XaHNFj
        self.SvoyjOb = SvoyjOb
        self.FJzohYF = FJzohYF
        self.adPFnLb = adPFnLb
        self.rjX = rjX
        self.FcQI = FcQI
        self.lwSINx = lwSINx
        self.SZoDZaC = SZoDZaC
        self.GuUbA = GuUbA


class SetAttrCls5(SetAttrBaseCls1):
    __slots__ = attrs

    def __init__(self, pwLF, pmYG, ncdv, umNRVn, Adyej, qrwxo, SltAK, qDv, pwLPZm, tVTRM, Edft, XaHNFj, SvoyjOb, FJzohYF, adPFnLb, rjX, FcQI, lwSINx, SZoDZaC, GuUbA):
        setattr(self, "pwLF", pwLF)
        setattr(self, "pmYG", pmYG)
        setattr(self, "ncdv", ncdv)
        setattr(self, "umNRVn", umNRVn)
        setattr(self, "Adyej", Adyej)
        setattr(self, "qrwxo", qrwxo)
        setattr(self, "SltAK", SltAK)
        setattr(self, "qDv", qDv)
        setattr(self, "pwLPZm", pwLPZm)
        setattr(self, "tVTRM", tVTRM)
        setattr(self, "Edft", Edft)
        setattr(self, "XaHNFj", XaHNFj)
        setattr(self, "SvoyjOb", SvoyjOb)
        setattr(self, "FJzohYF", FJzohYF)
        setattr(self, "adPFnLb", adPFnLb)
        setattr(self, "rjX", rjX)
        setattr(self, "FcQI", FcQI)
        setattr(self, "lwSINx", lwSINx)
        setattr(self, "SZoDZaC", SZoDZaC)
        setattr(self, "GuUbA", GuUbA)

class ManualCls1():
    __slots__ = attrs

    def __init__(self, pwLF, pmYG, ncdv, umNRVn, Adyej, qrwxo, SltAK, qDv, pwLPZm, tVTRM, Edft, XaHNFj, SvoyjOb, FJzohYF, adPFnLb, rjX, FcQI, lwSINx, SZoDZaC, GuUbA):
        self.pwLF = pwLF
        self.pmYG = pmYG
        self.ncdv = ncdv
        self.umNRVn = umNRVn
        self.Adyej = Adyej
        self.qrwxo = qrwxo
        self.SltAK = SltAK
        self.qDv = qDv
        self.pwLPZm = pwLPZm
        self.tVTRM = tVTRM
        self.Edft = Edft
        self.XaHNFj = XaHNFj
        self.SvoyjOb = SvoyjOb
        self.FJzohYF = FJzohYF
        self.adPFnLb = adPFnLb
        self.rjX = rjX
        self.FcQI = FcQI
        self.lwSINx = lwSINx
        self.SZoDZaC = SZoDZaC
        self.GuUbA = GuUbA


class ManualCls2():
    def __init__(self, pwLF, pmYG, ncdv, umNRVn, Adyej, qrwxo, SltAK, qDv, pwLPZm, tVTRM, Edft, XaHNFj, SvoyjOb, FJzohYF, adPFnLb, rjX, FcQI, lwSINx, SZoDZaC, GuUbA):
        self.pwLF = pwLF
        self.pmYG = pmYG
        self.ncdv = ncdv
        self.umNRVn = umNRVn
        self.Adyej = Adyej
        self.qrwxo = qrwxo
        self.SltAK = SltAK
        self.qDv = qDv
        self.pwLPZm = pwLPZm
        self.tVTRM = tVTRM
        self.Edft = Edft
        self.XaHNFj = XaHNFj
        self.SvoyjOb = SvoyjOb
        self.FJzohYF = FJzohYF
        self.adPFnLb = adPFnLb
        self.rjX = rjX
        self.FcQI = FcQI
        self.lwSINx = lwSINx
        self.SZoDZaC = SZoDZaC
        self.GuUbA = GuUbA

# fmt: on


@dataclass
class SetupArgs(BenchSetup):
    approach: str
    number: int

    def get_bench_name(self):
        return f"setattr2_{self.number}"

    def get_method_name(self) -> str:
        return f"{self.approach}_{self.number}"

    def get_setup(self):
        module = get_module(__file__)
        return "\n".join(
            [
                f"from {module} import {self.approach}",
                f"records = [list(range({len(attrs)})) for i in range({self.number})]",
            ]
        )

    def get_statement(self):
        if self.approach == "SetAttrCls3":
            args = ",".join([f"{a}=x[{i}]" for i, a in enumerate(attrs)])
        else:
            args = ",".join([f"x[{i}]" for i in range(len(attrs))])
        return f"[{self.approach}({args}) for x in records]"

    @staticmethod
    def iter_configs(default_cfg: dict) -> Iterator[BenchSetup]:
        for approach in [
            "ManualCls1",
            "ManualCls2",
            "SetAttrCls1",
            "SetAttrCls2",
            "SetAttrCls3",
            "SetAttrCls4",
            "SetAttrCls5",
        ]:
            yield SetupArgs(approach=approach, number=default_cfg.get("number", 10000))
