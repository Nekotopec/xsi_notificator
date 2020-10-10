import redis

from serializer import Ad, get_serializer

r = redis.Redis(host='localhost', port=6379, db=0)


def redis_set(key: str, value: str) -> None:
    r.set(key, value)


def redis_get(key: str) -> bytes:
    return r.get(key)


if __name__ == '__main__':
    ad = Ad(number='9659659659',
            link='https://yandex.ru',
            address='Тупа центр')
    serializer = get_serializer()
    key, value = serializer.serialize(ad)
    redis_set(key, value)
