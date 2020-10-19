import redis

from server.serializer import Ad, get_serializer

r = redis.Redis(host='redis', port=6379, db=0)


class DatabaseException(Exception):
    pass


class RedisException(DatabaseException):
    """Exception with redis."""
    pass


class RedisSetException(RedisException):
    """Exception occurred while setting."""
    pass


class RedisGetException(RedisException):
    """Exception occurred while getting."""
    pass


class RedisDeleteException(RedisException):
    """Exception occurred while deleting."""
    pass


def redis_set(key: str, value: str) -> None:
    try:
        r.set(key, value)
    except redis.RedisError:
        raise RedisSetException


def redis_delete(key: str):
    try:
        r.delete(key)
    except redis.RedisError:
        raise RedisDeleteException


def redis_get(key: str) -> bytes:
    try:
        return r.get(key)
    except redis.RedisError:
        raise RedisGetException


if __name__ == '__main__':
    ad = Ad(number='9659659659',
            link='https://yandex.ru',
            address='Тупа центр')
    serializer = get_serializer()
    key, value = serializer.serialize(ad)
    redis_set(key, value)
