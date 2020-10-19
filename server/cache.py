import logging

from pymemcache import Client, MemcacheError

client = Client(('memcached', 11211))


def cache_set(key: str, value: str):
    try:
        client.set(key, value, expire=130)
    except MemcacheError:
        logging.exception('Exception while cache_setting occurred.')


def cache_get(key):
    try:
        data = client.get(key)
    except MemcacheError:

        logging.exception('Exception while cache_getting occurred.')
        data = None

    if data:
        return data.decode()
    else:
        return None
