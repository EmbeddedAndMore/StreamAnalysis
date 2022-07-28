from __future__ import annotations
from abc import ABC
from enum import Enum, auto
from typing import Any

import numpy as np


class BaseDataLoader(ABC):
    def provide(self) -> Any:
        ...

    def post_process(self, data: Any) -> Any:
        ...


class ProcessorStage(Enum):
    PENDING = auto()
    PREPROCESS = auto()
    PROCESS = auto()
    POSTPROCESS = auto()


class BaseProcessor(ABC):
    def pre_process(self, data: Any) -> Any:
        ...

    def process(self, data: Any, *args, **kwargs) -> Any:
        ...

    def post_process(self, data: Any) -> Any:
        ...


class PipelineStage(Enum):
    PENDING = auto()
    PROVIDE_DATA = auto()
    PROCESS = auto()
    FINALIZE = auto()
    FINISHED = auto()


class BasePipeline(ABC):

    data_loader: BaseDataLoader
    processor: BaseProcessor

    def setup(self, config: dict) -> None:
        ...

    def execute(self) -> None:
        ...
