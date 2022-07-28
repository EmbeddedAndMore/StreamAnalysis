import numpy as np
import dramatiq
from dramatiq.brokers.redis import RedisBroker

from dramatiq.encoder import PickleEncoder
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.encoder import JSONEncoder, MessageData

r_broker = RedisBroker(url="redis://localhost", port=6379, db=0)
r_backend = RedisBackend(encoder=PickleEncoder())
r_broker.add_middleware(Results(backend=r_backend))

dramatiq.set_broker(r_broker)
dramatiq.set_encoder(JSONEncoder())
