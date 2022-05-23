import json
import random

from bots_settings.settings import redis_instance


class InlineCallbacks:
    @staticmethod
    def __get_rand() -> int:
        return random.randint(1, 123456789012345678901234567890)

    @staticmethod
    def set(callback: dict) -> int:
        callback_str = json.dumps(callback)
        val = InlineCallbacks.__get_rand()
        if not redis_instance.get(val):
            redis_instance.set(val, callback_str)
            return val
        else:
            return InlineCallbacks.set(callback)

    @staticmethod
    def get(value: int) -> dict:
        callback_str = redis_instance.get(value)
        if callback_str:
            callback = json.loads(callback_str)

            redis_instance.delete(value)
            return callback

        return None
