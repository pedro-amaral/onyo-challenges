import requests
from django.utils.six import BytesIO
from rest_framework import status
from rest_framework.parsers import JSONParser
from Ana.exceptions import BobServiceUnavailable, BobServiceLottoWithoutResult
from Ana.settings import BOB_BASE_ENDPOINT as ENDPOINT


cache = {}


class BobHelper:
    """
    Encapsulates functions with requests to Bob
    """
    @staticmethod
    def check_next_lotto() -> int:
        """
        Requests to Bob the next lotto identifier
        :return: identifier of the next Lotto (int)
        :raises BobServiceUnavailable: case Bob is offline
        """
        try:
            response = requests.get(ENDPOINT + 'next_lotto/', timeout=(1, 1))
            return int(JSONParser().parse(BytesIO(response.content)).get('next'))
        except requests.RequestException:
            raise BobServiceUnavailable

    @staticmethod
    def is_a_winner_ticket(ticket_id: int, lotto_id: int, bet: str) -> bool:
        # If the request has been cached return the result from here
        """
        Checks if the current ticket is a winner of the related lotto requesting information to Bob
        :param ticket_id: ticket identifier
        :param lotto_id: lotto identifier
        :param bet: the numbers of the bet
        :return: if is a winner ticket or not (bool)
        """
        if ticket_id in cache:
            return cache[ticket_id]
        try:
            response = requests.get(ENDPOINT + '{}/matches_winner'.format(lotto_id), params={'bet': bet},
                                    timeout=(1, 1))
            if response.status_code == status.HTTP_200_OK:
                is_a_winner = bool(JSONParser().parse(BytesIO(response.content)).get('matches'))
                cache.update({ticket_id: is_a_winner})
                return is_a_winner
            raise BobServiceLottoWithoutResult
        except requests.RequestException:
            raise BobServiceUnavailable
