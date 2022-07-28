from __future__ import annotations

import sched
import time
import queue
from time import perf_counter, sleep
from typing import Callable, Any
from threading import Thread
from collections import Counter


import numpy as np
import matplotlib.pyplot as plt
from dramatiq import Actor
from datasets import load_dataset

from ..analysis_base.base import BaseDataLoader, BaseProcessor
from ..dramatiq_app import r_broker


class WordFrequencyDataLoader(BaseDataLoader):
    def __init__(self, config: dict, data_ready: Callable):
        self.n_samples = config["samples"]
        self.overlap = config["overlap"]
        self.within = config["within"]
        self.queue_buffer = []
        self.callback_queue = queue.Queue()
        self.data_ready = data_ready
        self.dataset = load_dataset("oscar", "unshuffled_deduplicated_en", split="train", streaming=True)
        self.thread = Thread(daemon=True, target=self.provide)
        self.thread.start()

    def _time_limit_elapsed(self):
        data = self._collect_data()
        self.data_ready(data)

    def _collect_data(self):
        data = self.queue_buffer[: self.n_samples]
        n_to_del = len(data) - self.overlap
        if n_to_del > 0:
            self.queue_buffer = self.queue_buffer[n_to_del:]
        return data

    def provide(self) -> Any:
        start = perf_counter()
        for item in self.dataset:
            self.queue_buffer.append(item)
            if len(self.queue_buffer) == self.n_samples:
                data = self._collect_data()
                print(f"Time elapsed: {perf_counter()-start}s")
                self.callback_queue.put(lambda: self.data_ready(data))
                start = perf_counter()
            sleep(0.5)

    @property
    def n_available(self):
        return len(self.queue_buffer)


class WordFrequencyProcessor(BaseProcessor, Actor):
    def __init__(self):
        super().__init__(
            fn=self.perform,
            broker=r_broker,
            actor_name=__class__.__name__,
            queue_name="default",
            priority=0,
            options={"store_results": True},
        )

    def process(self, data: Any, name: str = "bar.jpg") -> Any:
        start = perf_counter()
        words = []
        for item in data:
            words.extend(item["text"].split())

        word_counts = Counter(words)
        plt.clf()
        plt.plot(range(len(word_counts)), word_counts.values())
        plt.savefig(f"data/{name}")
        print(f"data saved! {perf_counter()-start}")

    def perform(self, data, name: str):
        self.process(data, name)


wf_processor = WordFrequencyProcessor()
