from server.serializer import Ad, get_serializer
import server.db as db

serializer = get_serializer()


class BaseException(Exception):
    pass


class BadParamsError(BaseException):
    """There is no needed key in data."""
    pass


def load_to_database(data: dict) -> bool:
    try:
        ad = build_ad(data)
    except KeyError:
        raise BadParamsError
    key, value = serializer.serialize(ad)
    try:
        db.redis_set(key, value)
        return True
    except db.RedisSetException:
        return False


def delete_ad(data: dict):
    """Delete ad from database by number."""
    try:
        key = data['number']
    except KeyError:
        raise BadParamsError
    try:
        db.redis_delete(key)
        return True
    except db.RedisDeleteException:
        return False


def build_ad(data: dict) -> Ad:
    link = data.get('link')
    return Ad(number=data['number'],
              address=data['address'],
              link=link)
