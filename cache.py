import logging

from pymemcache import Client, MemcacheError

client = Client(('127.0.0.1', 11211))


def cache_set(key: str, value: str):
    try:
        client.set(key, value, expire=130)
    except MemcacheError:
        logging.exception('Exception while cache_setting occurred.')


def cache_get(key):
    data = client.get(key)
    if data:
        return data.decode()
    else:
        return None
