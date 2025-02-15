import pickle

import redis

from pick.pick import Pick


class RedisHandler:
    Connection : redis.Redis
    PickChannel : str

    def __init__(self, host, port, db):
        self.Connection = redis.Redis(host, port, db)
        self.PickChannel = "PickChannel"

    def emit_pick_message(self, pick : Pick):
        self.Connection.publish(self.PickChannel, pickle.dumps(pick))
