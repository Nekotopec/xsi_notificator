from cache import cache_get, cache_set
from parser import CallInfo


def check_notification(call_info: CallInfo) -> bool:
    """
    Checks if a call was received from the call_info.calling_number.
    """
    value = cache_get(call_info.calling_number[1:])
    if value == call_info.redirecting_number[1:]:
        return False
    else:
        return True


def remember_number(call_info: CallInfo) -> None:
    """
    Remember calling number for 60 seconds in cache.
    """
    cache_set(call_info.calling_number[1:], call_info.redirecting_number[1:])

