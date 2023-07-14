from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import benchpyo3.core as pyo3

from pybench.base import BenchSetup
from pybench.helper import get_module


class Method:
    create_range__ru_1 = pyo3.create_range_1
    create_range__ru_2 = pyo3.create_range_2
    create_range__ru_3 = pyo3.create_range_3
    create_range__ru_4 = pyo3.create_range_4

    @staticmethod
    def create_range__py_1(n: int):
        return list(range(n))

    @staticmethod
    def create_range__py_2(n: int):
        return [i for i in range(n)]


@dataclass
class BenchRunPyInRust(BenchSetup):
    method: str
    size: int

    def get_bench_name(self) -> str:
        return self.method.split("__")[0] + "_" + str(self.size)

    def get_method_name(self) -> str:
        return self.method

    def get_setup(self):
        module = get_module(__file__)
        return "\n".join([f"from {module} import Method", f"fn = Method.{self.method}"])

    def get_statement(self):
        if self.method.startswith("create_range"):
            return f"fn({self.size})"

    @staticmethod
    def iter_configs(default_cfg: dict) -> Iterator[BenchRunPyInRust]:
        for size in [100, 1000, 5000]:
            for method in [
                "create_range__py_1",
                "create_range__py_2",
                "create_range__ru_1",
                "create_range__ru_2",
                "create_range__ru_3",
                "create_range__ru_4",
            ]:
                yield BenchRunPyInRust(method=method, size=size)
