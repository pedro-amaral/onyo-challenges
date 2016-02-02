from io import BytesIO
from django.contrib.auth.models import User
from unittest import TestCase
from mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.parsers import JSONParser
from Ana.models import BetTicket


class BetTicketViewTest(TestCase):
    user = None
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user('test', '', 'test')
        cls.client.force_authenticate(cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    @patch('requests.get')
    def test__is_a_winner__success_winner_ticket(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, content=b'{"matches": true}')
        ticket = BetTicket.objects.create(bet='1 2 3 4 5 6', owner=self.user, lotto_id=1)

        response = self.client.get('/bets/{}/is_a_winner/'.format(ticket.id), format='json')
        response.render()

        self.assertEqual(bool(JSONParser().parse(BytesIO(response.content))), True)

    @patch('requests.get')
    def test__is_a_winner__success_not_a_winner_ticket(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, content=b'{"matches": false}')
        ticket = BetTicket.objects.create(bet='1 2 3 4 5 6', owner=self.user, lotto_id=2)

        response = self.client.get('/bets/{}/is_a_winner/'.format(ticket.id), format='json')
        response.render()

        self.assertEqual(bool(JSONParser().parse(BytesIO(response.content))), False)

    @patch('requests.get')
    def test__is_a_winner__failed_bob_without_result(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)
        ticket = BetTicket.objects.create(bet='1 2 3 4 5 10', owner=self.user, lotto_id=5, id=10)

        response = self.client.get('/bets/{}/is_a_winner/'.format(ticket.id), format='json')
        response.render()

        self.assertEqual(bool(JSONParser().parse(BytesIO(response.content))), 'The result of the request Lotto is not '
                                                                              'available yet.')

    def test__is_a_winner_with_post__failed_method_not_allowed(self):
        response = self.client.post('/bets/1/is_a_winner/', format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__is_a_winner_with_put__failed_method_not_allowed(self):
        response = self.client.put('/bets/1/is_a_winner/', format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__is_a_winner_with_not_owner_user__failed_forbidden(self):
        ticket = BetTicket.objects.create(bet='1 2 3 4 5 8', owner=self.user, lotto_id=1)

        user = User.objects.create_user('test_not_owner', '', 'test')

        self.client.force_authenticate(user=user)

        response = self.client.get('/bets/{}/is_a_winner/'.format(ticket.id), format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



