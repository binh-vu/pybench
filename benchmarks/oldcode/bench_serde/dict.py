from __future__ import annotations

import pickle
import random
from dataclasses import asdict, dataclass
from typing import Dict, Iterator, Literal, Tuple

import orjson

from pybench.base import BenchSetup
from pybench.generators import GaussGenerators
from pybench.helper import get_module


@dataclass
class CellIndexDict:
    ntbls: int
    nrows: int
    ncols: int

    def get_dict(
        self,
    ) -> Dict[
        str, Tuple[int, int, Dict[int, Tuple[int, int, Dict[int, Tuple[int, int]]]]]
    ]:
        strkey = False
        table = {}
        gen = GaussGenerators(72)
        lst = gen.strings(self.ntbls, avglen=10)
        for s in lst:
            cols = {}
            table[s] = (random.randint(0, 1000), random.randint(0, 1000), cols)

            for i in range(gen.integers(1, self.ncols, 2)[0]):
                rows = {}
                k = str(i) if strkey else i
                cols[k] = (random.randint(0, 1000), random.randint(0, 1000), rows)
                for j in range(gen.integers(1, self.nrows, 2)[0]):
                    k = str(j) if strkey else j
                    rows[k] = (random.randint(0, 1000), random.randint(0, 1000))
        return table

    @staticmethod
    def dumps(method: str, obj):
        if method == "pickle":
            return pickle.dumps(obj)
        if method == "orjson2":
            return orjson.dumps(obj, option=orjson.OPT_NON_STR_KEYS)
        if method == "orjson":
            # fmt: off
            return orjson.dumps([
                (tid, tstart, tend, [
                    (cid, cstart, cend, [
                        (rid, rstart, rend)
                        for rid, (rstart, rend) in cindex.items()
                    ])
                    for cid, (cstart, cend, cindex) in tindex.items()
                ])
                for tid, (tstart, tend, tindex) in obj.items()
            ])
            # fmt: on
        assert False

    @staticmethod
    def loads(method, obj):
        if method == "pickle":
            return pickle.loads(obj)
        if method == "orjson2":
            obj = orjson.loads(obj)
            for x in obj.values():
                x[-1] = {int(k): v for k, v in x[-1].items()}
                for y in x[-1].values():
                    y[-1] = {int(k): v for k, v in y[-1].items()}
            return obj
        if method == "orjson":
            # fmt: off
            return {
                tid: (tstart, tend, {
                    cid: (cstart, cend, {
                        rid: (rstart, rend)
                        for rid, rstart, rend in cindex
                    })
                    for cid, cstart, cend, cindex in tindex
                })
                for tid, tstart, tend, tindex in orjson.loads(obj)
            }
            # fmt: on

        assert False


@dataclass
class SetupArgs(BenchSetup):
    method: str
    serde: Literal["ser", "de"]
    dictfactory: CellIndexDict

    def get_bench_name(self):
        args = "_".join([f"{k}_{v}" for k, v in asdict(self.dictfactory).items()])
        return f"{self.dictfactory.__class__.__name__.lower()}_{args.lower()}"

    def get_method_name(self):
        return (
            f"{self.method}_{self.serde}_{self.dictfactory.__class__.__name__.lower()}"
        )

    def get_setup(self):
        module = get_module(__file__)
        clsname = self.dictfactory.__class__.__name__
        args = orjson.dumps(asdict(self.dictfactory)).decode()
        return "\n".join(
            [
                f"from {module} import {clsname}",
                "import pickle, orjson",
                f"obj = {clsname}(**{args}).get_dict()",
                f"obj = {clsname}.dumps('{self.method}', obj)"
                if self.serde == "de"
                else "",
            ]
        )

    def get_statement(self):
        clsname = self.dictfactory.__class__.__name__
        serde = "dumps" if self.serde == "ser" else "loads"
        return f"a = {clsname}.{serde}('{self.method}', obj)"

    @staticmethod
    def iter_configs(default_cfg: dict) -> Iterator[BenchSetup]:
        for method in ["pickle", "orjson", "orjson2"]:
            for serde in ["ser", "de"]:
                yield SetupArgs(
                    method=method,
                    serde=serde,  # type: ignore
                    dictfactory=CellIndexDict(ntbls=1000, nrows=40, ncols=10),
                )
