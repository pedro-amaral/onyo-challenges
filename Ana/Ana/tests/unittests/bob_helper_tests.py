import requests
from mock import patch, MagicMock
from unittest import TestCase
from Ana.utils import BobHelper
from Ana.exceptions import BobServiceUnavailable, BobServiceLottoWithoutResult


class BobHelperTest(TestCase):
    @patch('requests.get')
    def test__check_next_lotto__success(self, mock_get):
        mock_get.return_value = MagicMock(content=b'{"next": 1}')

        next_lotto_id = BobHelper.check_next_lotto()

        self.assertEqual(next_lotto_id, 1)

    @patch('requests.get')
    def test__check_next_lotto_bob_offline__raises_bob_unavailable(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()

        self.assertRaises(BobServiceUnavailable, BobHelper.check_next_lotto)

    @patch('requests.get')
    def test__is_a_winner_ticket__success_winner_ticket(self, mock_get):
        mock_get.return_value = MagicMock(content=b'{"matches": true}', status_code=200)

        is_a_winner = BobHelper.is_a_winner_ticket(1, 1, '1 2 3 4 5 6')

        self.assertTrue(is_a_winner)

    @patch('requests.get')
    def test__is_a_winner_ticket_lotto_without_result__raises_bob_without_result(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)

        self.assertRaises(BobServiceLottoWithoutResult, BobHelper.is_a_winner_ticket, ticket_id=2, lotto_id=1,
                          bet='1 1 1 1 1 1')

    @patch('requests.get')
    def test__is_a_winner_ticket_bob_offline__raises_bob_unavailable(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()

        self.assertRaises(BobServiceUnavailable, BobHelper.is_a_winner_ticket, ticket_id=3, lotto_id=1,
                          bet='1 1 1 1 1 1')
