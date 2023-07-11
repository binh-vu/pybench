from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import benchpyo3.core  # type: ignore
import orjson
import serde.jl
import serde.textline

from pybench.base import BenchSetup
from pybench.helper import get_module

RESOURCE_DIR = Path(__file__).parent.parent.parent / "resources"


@dataclass
class PythonEntityLabel:
    id: str
    label: dict[str, str]

    @staticmethod
    def from_json(json: str):
        return PythonEntityLabel(**orjson.loads(json))

    def doing_nothing(self):
        ...

    def get_wikidata_numeric_id(self):
        return int(self.id[1:])

    def return_5(self):
        return 5

    def get_n_labels(self):
        return len(self.label)


RustEntityLabel = benchpyo3.core.EntityLabel
RustFrozenEntityLabel = benchpyo3.core.FrozenEntityLabel


@dataclass
class BenchObjectCall(BenchSetup):
    bench: str
    method: str

    def get_bench_name(self) -> str:
        return self.bench

    def get_method_name(self) -> str:
        return self.method

    def get_setup(self):
        module = get_module(__file__)
        return "\n".join(
            [
                f"from {module} import RESOURCE_DIR",
                "import serde.textline, serde.jl",
                f"from {module} import {self.method}EntityLabel",
                f"EntityLabel = {self.method}EntityLabel",
                "texts = serde.textline.deser(RESOURCE_DIR / 'entity_labels.jl.gz')",
                "objects = serde.jl.deser(RESOURCE_DIR / 'entity_labels.jl.gz')",
                "text0 = texts[0]",
                "text1 = texts[1]",
                "text2 = texts[2]",
                "obj0 = objects[0]",
                "obj1 = objects[1]",
                "instance0 = EntityLabel.from_json(text0)",
                "instance1 = EntityLabel.from_json(text1)",
            ]
        )

    def get_statement(self):
        if self.bench == "from_json":
            return f"EntityLabel.from_json(text2)"
        return f"instance0.{self.bench}()"

    @staticmethod
    def iter_configs(default_cfg: dict) -> Iterator[BenchObjectCall]:
        for method in ["Rust", "Python", "RustFrozen"]:
            for bench in [
                "from_json",
                "doing_nothing",
                "return_5",
                "get_wikidata_numeric_id",
            ]:
                yield BenchObjectCall(
                    bench=bench,
                    method=method,
                )
