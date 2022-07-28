from __future__ import annotations

import queue
from time import sleep
import threading

from .stream_analysis_pipeline.word_frequency_pipeline import WordFrequencyDataLoader, wf_processor

configs = {"samples": 3, "overlap": 1, "within": 5000}

arrived = 0
sent_messages = []


def data_is_ready(result: list):
    global arrived
    global sent_messages
    print("thread:", threading.currentThread().name)
    cnt = 0
    while cnt < 10000000:
        cnt += 1
    for item in result:
        arrived += 1
        print(f"arrived: {item['id']}-{item['text'][:50]}")

    name = f"{result[0]['id']}.jpg"
    sent_messages.append(wf_processor.send(result, name))


if __name__ == "__main__":
    sa_loader = WordFrequencyDataLoader(configs, data_is_ready)

    def callback():
        return None

    while True:
        try:
            callback = sa_loader.callback_queue.get(block=False)
        except queue.Empty:
            print("Data not ready")
            sleep(0.1)
            continue
        callback()
        print(
            f"Loaded: {sa_loader.n_available}, Processed: {arrived}, not_processed: {sa_loader.callback_queue.qsize()}"
        )
        sleep(0.1)
