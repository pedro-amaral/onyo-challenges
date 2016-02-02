from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITransactionTestCase, APIClient
from Ana.models import BetTicket


class GeneralTest(APITransactionTestCase):
    user = None
    client = APIClient()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('test', '', 'test')
        self.client.force_authenticate(self.user)

    def tearDown(self):
        super().tearDown()

    def test__create_bet_ticket__success(self):
        data = {'bet': '1 2 3 4 5 6', 'lotto_id': 1}

        response = self.client.post('/bets/', data, format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BetTicket.objects.count(), 1)
        self.assertEqual(BetTicket.objects.get().bet, data.get('bet'))

    def test__create_bet_ticket_missing_authentication__failed(self):
        self.client.force_authenticate(user=None)
        data = {'bet': '1 2 3 4 5 6', 'lotto_id': 1}

        response = self.client.post('/bets/', data, format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BetTicket.objects.count(), 0)

    def test__update_a_bet_ticket__failed_method_not_allowed(self):
        ticket = BetTicket.objects.create(bet='1 2 3 4 5 6', lotto_id=1, owner=self.user)
        data = {'bet': '1 1 1 1 1 1'}

        response = self.client.put('/bets/{}/'.format(ticket.id), data, format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotEqual(BetTicket.objects.get().bet, data.get('bet'))

    def test__delete_a_bet_ticket__failed_method_not_allowed(self):
        ticket = BetTicket.objects.create(bet='1 2 3 4 5 6', lotto_id=1, owner=self.user)

        response = self.client.delete('/bets/{}/'.format(ticket.id), format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(BetTicket.objects.count(), 1)
