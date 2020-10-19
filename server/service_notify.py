import logging
from typing import Union

import server.db as db
import server.notifications_filter as notifications_filter
import server.parser as parser
from server.notifier import get_notifiers_list
from server.serializer import Ad, get_serializer

serializer = get_serializer()
notifiers_list = get_notifiers_list()


async def notify(message):
    """
    Make all notifiers notify.
    """

    for notifier in notifiers_list:
        try:
            await notifier.notify(message)
        except Exception:
            logging.exception('While notify exception was accurred.')


def write_log(data):
    with open('Xsi_event.txt', 'a') as f:
        message = ('================================\n'
                   f'{data}\n'
                   '================================\n')
        f.write(message)


def format_message(call_info: parser.CallInfo, add: Union[Ad, None]) -> str:
    """
    Format message with info from call_info.
    """

    message = (f'Номер звонящего: {call_info.calling_number} \n'
               f'Номер переадресации: {call_info.redirecting_number} \n')
    if add is not None:
        add_mess = (
            f'Адрес: {add.address}\n'
            f'Ссылка на объявление: \"<a href=\"{add.link}\">Ссылка</a>\"'
        )
        message = message + add_mess

    return message


def get_ad_by_number(number: str):
    """ Returns Ad class's instance by number or None."""
    try:
        raw_data = db.redis_get(number)
    except db.RedisGetException:
        raw_data = None
    if raw_data is not None:
        return serializer.deserialize(number, raw_data)
    else:
        return None


async def send_info(data: str):
    """
    Get info from xsi notify and send it trow notifiers.
    """

    event_parser = parser.get_parser()
    call_info = event_parser.get_info(data)
    if call_info:
        if notifications_filter.check_notification(call_info):
            notifications_filter.remember_number(call_info)
            ad = get_ad_by_number(call_info.redirecting_number)
            message = format_message(call_info, ad)
            logging.info(message)
            await notify(message)
