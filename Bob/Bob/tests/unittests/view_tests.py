from io import BytesIO
from django.contrib.auth.models import User
from unittest import TestCase
from mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.parsers import JSONParser
from Bob.models import LottoResult


class LottoResultViewTest(TestCase):
    user = None
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user('test', '', 'test')
        cls.client.force_authenticate(cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    @patch('django.db.models.query.QuerySet.last')
    def test__next_lotto_with_empty_table__success_first_lotto(self, mock_last):
        mock_last.return_value = None

        response = self.client.get('/lotto-results/next_lotto/', format='json')
        response.render()

        self.assertEqual(int(JSONParser().parse(BytesIO(response.content)).get('next')), 1)

    @patch('django.db.models.query.QuerySet.last')
    def test__next_lotto__success(self, mock_last):
        mock_last.return_value = LottoResult(id=1)

        response = self.client.get('/lotto-results/next_lotto/', format='json')
        response.render()

        self.assertEqual(int(JSONParser().parse(BytesIO(response.content)).get('next')), 2)

    def test__next_lotto_with_post__failed_method_not_allowed(self):
        response = self.client.post('/lotto-results/next_lotto/', format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__next_lotto_with_put__failed_method_not_allowed(self):
        response = self.client.put('/lotto-results/next_lotto/', format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__matches_winner__success(self):
        lotto = LottoResult.objects.create(title='Test Lotto')
        bet = lotto.result

        response = self.client.get('/lotto-results/{}/matches_winner/'.format(lotto.id), data={"bet": bet})
        response.render()

        self.assertTrue(bool(JSONParser().parse(BytesIO(response.content)).get('matches')))

    def test__matches_winner_with_unordered_bet__success(self):
        lotto = LottoResult.objects.create(title='Test Lotto')
        bet = ' '.join(lotto.result.split(' ')[::-1])

        response = self.client.get('/lotto-results/{}/matches_winner/'.format(lotto.id), data={"bet": bet})
        response.render()

        self.assertTrue(bool(JSONParser().parse(BytesIO(response.content)).get('matches')))

    def test__matches_winner_return_false__success(self):
        lotto = LottoResult.objects.create(title='Test Lotto')
        bet = '1 1 1 2 2 2'

        response = self.client.get('/lotto-results/{}/matches_winner/'.format(lotto.id), data={"bet": bet})
        response.render()

        self.assertFalse(bool(JSONParser().parse(BytesIO(response.content)).get('matches')))

    def test__matches_winner_with_empty_bet__failed_bad_request(self):
        lotto = LottoResult.objects.create(title='Test Lotto')

        response = self.client.get('/lotto-results/{}/matches_winner/'.format(lotto.id))
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test__matches_winner_bet_missing_numbers__failed_bad_request(self):
        lotto = LottoResult.objects.create(title='Test Lotto')

        response = self.client.get('/lotto-results/{}/matches_winner/'.format(lotto.id), params={'bet': '1 2 3'})
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
