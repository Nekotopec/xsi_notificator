import json
from abc import ABC, abstractmethod
from typing import NamedTuple, Tuple


class Ad(NamedTuple):
    number: str
    link: str
    address: str


class AbstractSerializer(ABC):

    @abstractmethod
    def serialize(self, obj) -> str:
        """Serialize python object for storage."""
        pass

    @abstractmethod
    def deserialize(self, key: str, value: bytes) -> object:
        """Deserialize storage object to python object."""
        pass


class JsonSerializer(AbstractSerializer):

    def serialize(self, obj) -> Tuple[str, str]:
        key, value = self.get_key_value(obj)
        return key, json.dumps(value)

    def deserialize(self, key, value: bytes) -> object:
        """Deserialize storage object to python object."""
        value = value.decode()
        return self.get_python_obj(key, value)

    @abstractmethod
    def get_key_value(self, obj) -> Tuple[str, dict]:
        """Build serializable objects."""
        pass

    @abstractmethod
    def get_python_obj(self, key: str, value: str):
        """Build python object."""
        pass


class AdJsonSerializer(JsonSerializer):
    """Serialize instances of class Ad."""

    def get_key_value(self, obj: Ad) -> Tuple[str, dict]:
        """Returns number as key and other as value."""

        key = obj.number
        value = {
            'link': obj.link,
            'address': obj.address
        }
        return key, value

    def get_python_obj(self, key: str, value: str):
        """Returns Ad class's instance."""
        val_dict = json.loads(value)
        return Ad(number=key,
                  link=val_dict['link'],
                  address=val_dict['address'])


def get_serializer():
    return AdJsonSerializer()
