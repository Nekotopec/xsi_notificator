import logging
from abc import ABC, abstractmethod
from typing import List

import aiohttp
import ujson

from config import read_config


class BaseError(Exception):
    pass


class NotifierWasNotRealised(BaseError):
    """ Notifier from settings.yaml was not realised yet."""
    pass


class NoNotifiersFound(BaseError):
    """There are no notifiers was found in settings.yml."""
    pass


class BadStatus(BaseError):
    """Not 200 status code from telegrram api was handled."""
    pass


class TelegramNotifierError(BaseError):
    """Error in telegram notifier."""
    pass


class ApiKeyDoesNotExistError(TelegramNotifierError):
    """Api key does not exist in the settings.yaml file."""
    pass


class ChatIdsDontExistError(TelegramNotifierError):
    """There are no chat ids in settings.yaml file."""
    pass


class AbstractNotifier(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def notify(self, message: str) -> None:
        """
        Notify about incoming call and send information about it.
        """

        pass


class AbstractNotifiersFactory(ABC):

    @classmethod
    @abstractmethod
    def create_notifier(cls) -> AbstractNotifier:
        """
        Create notifier instance.
        """
        pass


class TelegramNotifier(AbstractNotifier):

    def __init__(self, api_key: str, chat_ids_list):
        super().__init__()
        self.api_key = api_key
        self.chat_ids_list = chat_ids_list
        self.api_url = self._get_api_url()

    def _get_api_url(self):
        """
        Returns api url with method sendMessage.
        """

        return f'https://api.telegram.org/bot{self.api_key}/sendMessage'

    async def notify(self, message: str):
        await self._send_messages(message)

    async def _send_messages(self, message: str) -> None:
        """
        Send message to all chat_ids in chat_id_list.
        """
        for chat_id in self.chat_ids_list:
            await self._send_request_to_api(message, chat_id)

    async def _send_request_to_api(self, message: str, chat_id: int):
        """
        Send message from telegram bot to user with chat_id.
        """
        headers = {
            'Content-Type': 'application/json'
        }
        message = {
            'text': message,
            'chat_id': chat_id,
            'parse_mode': 'HTML'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url,
                                    data=ujson.dumps(message),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except AssertionError:
                    logging.exception(
                        'Exception was occurred while sending message.'
                    )


class TelegramNotifierFactory(AbstractNotifiersFactory):

    @classmethod
    def create_notifier(cls) -> TelegramNotifier:
        """
        Create TelegramNotifier.
        """
        api_key = cls._get_api_key()
        chat_id_list = cls._get_chat_id_list()
        return TelegramNotifier(api_key, chat_id_list)

    @staticmethod
    def _get_api_key():
        """
        Returns api key from file settings.yaml.
        """
        cfg = read_config()
        cfg = cfg['notifier']['telegram_bot']
        return cfg.get('api_key')

    @staticmethod
    def _get_chat_id_list():
        """
        Returns list of chat_id from file settings.yaml.
        """
        cfg = read_config()
        cfg = cfg['notifier']['telegram_bot']
        return cfg.get('chat_id')


notifiers_fabrics_dict = {
    'telegram_bot': TelegramNotifierFactory
}


def get_notifiers_list() -> List[AbstractNotifier]:
    """
    Returns notifier using conf file.
    """

    cfg = read_config()
    notifiers = cfg.get('notifier')
    notifiers_list = list()
    for notifier in notifiers:
        notifier_fabric = notifiers_fabrics_dict.get(str(notifier))
        if notifier_fabric:
            notifier = notifier_fabric.create_notifier()
            notifiers_list.append(notifier)
        else:
            raise NotifierWasNotRealised

    if len(notifiers_list) < 0:
        raise NoNotifiersFound
    return notifiers_list
