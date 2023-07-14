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
class NumericId:
    id: int

    def is_even(self):
        return self.id % 2 == 0


class Python:
    @staticmethod
    def doing_nothing():
        ...

    @staticmethod
    def return_5():
        return 5

    @staticmethod
    def get_wikidata_numeric_id(id: str):
        return int(id[1:])

    @staticmethod
    def get_n_labels(text: str):
        return len(orjson.loads(text)["label"])

    @staticmethod
    def uppercase(s: str):
        return s.upper()

    @staticmethod
    def get_text_len(s: str):
        return len(s)

    @staticmethod
    def create_numeric_id(id: int):
        return NumericId(id)

    @staticmethod
    def create_numeric_id_2(id: int):
        return id

    @staticmethod
    def is_numeric_id_even(id: int) -> bool:
        return NumericId(id).is_even()

    @staticmethod
    def is_numeric_id_even_2(id: int) -> bool:
        return id % 2 == 0

    @staticmethod
    def is_numeric_id_even_3(id: int) -> bool:
        return id % 2 == 0


class Rust:
    doing_nothing = benchpyo3.core.doing_nothing
    return_5 = benchpyo3.core.return_5
    get_wikidata_numeric_id = benchpyo3.core.get_wikidata_numeric_id
    get_n_labels = benchpyo3.core.get_n_labels
    uppercase = benchpyo3.core.uppercase
    get_text_len = benchpyo3.core.get_text_len
    create_numeric_id = benchpyo3.core.create_numeric_id
    create_numeric_id_2 = benchpyo3.core.create_numeric_id_2
    is_numeric_id_even = benchpyo3.core.is_numeric_id_even
    is_numeric_id_even_2 = benchpyo3.core.is_numeric_id_even_2
    is_numeric_id_even_3 = benchpyo3.core.is_numeric_id_even_3
    create_range = benchpyo3.core.create_range


@dataclass
class BenchFnCall(BenchSetup):
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
                f"from {module} import {self.method}, RESOURCE_DIR",
                "import serde.textline, serde.jl",
                f"fn = {self.method}.{self.bench}",
                "texts = serde.textline.deser(RESOURCE_DIR / 'entity_labels.jl.gz')",
                "objects = serde.jl.deser(RESOURCE_DIR / 'entity_labels.jl.gz')",
                "text0 = texts[0]",
                "text1 = texts[1]",
                "obj0 = objects[0]",
                "obj1 = objects[1]",
                "id0 = int(obj0['id'][1:])",
            ]
        )

    def get_statement(self):
        if self.bench in ["doing_nothing", "return_5"]:
            return "fn()"
        if self.bench == "get_wikidata_numeric_id":
            return "fn(obj0['id'])"
        if self.bench in [
            "create_numeric_id",
            "create_numeric_id_2",
            "is_numeric_id_even",
            "is_numeric_id_even_2",
            "is_numeric_id_even_3",
        ]:
            return "fn(id0)"
        if self.bench in ["get_n_labels", "uppercase", "get_text_len"]:
            return "fn(text0)"
        assert False

    @staticmethod
    def iter_configs(default_cfg: dict) -> Iterator[BenchFnCall]:
        for bench in [
            "doing_nothing",
            "return_5",
            "get_wikidata_numeric_id",
            "get_n_labels",
            "uppercase",
            "get_text_len",
            "create_numeric_id",
            "create_numeric_id_2",
            "is_numeric_id_even",
            "is_numeric_id_even_2",
            "is_numeric_id_even_3",
        ]:
            for method in ["Rust", "Python"]:
                yield BenchFnCall(
                    bench=bench,
                    method=method,
                )
