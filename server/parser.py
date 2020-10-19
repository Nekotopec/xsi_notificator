import re
from abc import ABC, abstractmethod
from typing import NamedTuple, Type, Union

from bs4 import BeautifulSoup


class BaseParserException(Exception):
    pass


class NotCallEventException(BaseParserException):
    """Exception occur when server get not call event info."""
    pass


class CallInfo(NamedTuple):
    event_id: str
    calling_number: str
    redirecting_number: str
    event_state: str


class AbstractParser(ABC):

    @classmethod
    @abstractmethod
    def get_info(cls, raw_data) -> Union[CallInfo, None]:
        """ Returns info about call."""
        pass


class XmlParser(AbstractParser):
    xml = 'lxml-xml'

    @classmethod
    def get_info(cls, raw_data):
        """ Returns info about call from xml raw data."""
        xml_soup = cls._get_soup(raw_data)
        try:
            call_info = cls._fetch_info(xml_soup)
        except NotCallEventException:
            return None

        return call_info

    @classmethod
    def _get_soup(cls, raw_data) -> BeautifulSoup:
        """
        Returns soup made with BeautifulSoup.
        """

        return BeautifulSoup(raw_data, cls.xml)

    @staticmethod
    def _check_event_state(event_state: str) -> bool:
        """
        Check event state.
        Returns True if event_state is "Alerting".
        Return False if event_state is not "Alerting".
        """
        return event_state.lower() == 'alerting'

    @classmethod
    def _fetch_info(cls, soup: BeautifulSoup) -> Union[CallInfo, None]:
        event_id = soup.find('xsi:eventID').text
        try:
            event_state = soup.find('xsi:state').text
        except AttributeError:
            raise NotCallEventException
        if cls._check_event_state(event_state):

            numbers = soup.find_all('xsi:address')
            calling_number = numbers[0].text[6:]
            redirecting_number = numbers[1].text[6:]
            return CallInfo(
                event_id=event_id,
                calling_number=calling_number,
                redirecting_number=redirecting_number,
                event_state=event_state
            )
        else:
            return None

    @staticmethod
    def _get_info_by_regexp(text) -> CallInfo:
        """
        На всякий.
        """

        event_id = re.findall(
            r'<xsi:eventID>([\d\w-]+)</xsi:eventID>',
            text)[0]
        numbers = re.findall(
            r'countryCode=\"\d\">tel:(\+\d+)</xsi:address>',
            text)
        calling_number = numbers[0]
        redirecting_number = numbers[1]
        return CallInfo(event_id=event_id,
                        calling_number=calling_number,
                        redirecting_number=redirecting_number)


def get_parser() -> Type[AbstractParser]:
    return XmlParser


if __name__ == '__main__':
    with open('xml_ex.txt', 'r') as f:
        text = f.read()
    data = XmlParser.get_info(text)
    print(data)
