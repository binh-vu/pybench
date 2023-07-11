from dataclasses import dataclass
from typing import Iterator

from pybench.base import BenchSetup
from pybench.helper import get_module

# fmt: off
attrs = ['pwLF', 'pmYG', 'ncdv']

class WithSlot:
    __slots__ = attrs

    def __init__(self, pwLF, pmYG, ncdv):
        self.pwLF = pwLF
        self.pmYG = pmYG
        self.ncdv = ncdv

class WithoutSlot:
    def __init__(self, pwLF, pmYG, ncdv):
        self.pwLF = pwLF
        self.pmYG = pmYG
        self.ncdv = ncdv

# fmt: on


@dataclass
class SetupArgs(BenchSetup):
    clsname: str
    method: str
    number: int

    def get_bench_name(self):
        return f"setattr_{self.number}"

    def get_method_name(self) -> str:
        return f"{self.clsname}_{self.method}_{self.number}"

    def get_setup(self):
        module = get_module(__file__)
        return "\n".join(
            [
                f"from {module} import {self.clsname}",
                f"obj = {self.clsname}(*list(range({len(attrs)})))",
                f"records = [list(range(i, i+{len(attrs)})) for i in range({self.number})]",
            ]
        )

    def get_statement(self):
        if self.method == "setattr":
            return "\n".join(
                [
                    f"for r in records:",
                    "\n".join(
                        [
                            f"    setattr(obj, '{attr}', r[{i}])"
                            for i, attr in enumerate(attrs)
                        ]
                    ),
                ]
            )
        if self.method == "manual":
            return "\n".join(
                [
                    f"for r in records:",
                    "\n".join(
                        [f"    obj.{attr} = r[{i}]" for i, attr in enumerate(attrs)]
                    ),
                ]
            )

    @staticmethod
    def iter_configs(default_cfg: dict) -> Iterator[BenchSetup]:
        for clsname in [
            "WithSlot",
            "WithoutSlot",
        ]:
            for method in ["manual", "setattr"]:
                yield SetupArgs(
                    clsname=clsname,
                    method=method,
                    number=default_cfg.get("number", 10000),
                )
