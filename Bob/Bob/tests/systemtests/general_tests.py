from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITransactionTestCase, APIClient
from Bob.models import LottoResult


class GeneralTest(APITransactionTestCase):
    user = None
    client = APIClient()

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('test', '', 'test')
        self.client.force_authenticate(self.user)

    def tearDown(self):
        super().tearDown()

    def test__create_lotto_result__success(self):
        data = {'title': 'Test Lotto'}

        response = self.client.post('/lotto-results/', data, format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LottoResult.objects.count(), 1)
        self.assertEqual(LottoResult.objects.get().title, data.get('title'))

    def test__create_lotto_result_missing_authentication__failed(self):
        self.client.force_authenticate(user=None)
        data = {'title': 'Test Lotto'}

        response = self.client.post('/lotto-results/', data, format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(LottoResult.objects.count(), 0)

    def test__update_a_lotto_result__failed_method_not_allowed(self):
        lotto_result = LottoResult.objects.create(title='Lotto Test')
        data = {'result': '1 2 3 4 5 6'}

        response = self.client.put('/lotto-results/{}/'.format(lotto_result.id), data, format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotEqual(LottoResult.objects.get().result, data.get('result'))

    def test__delete_a_lotto_result__failed_method_not_allowed(self):
        lotto_result = LottoResult.objects.create(title='Lotto Test')

        response = self.client.delete('/lotto-results/{}/'.format(lotto_result.id), format='json')
        response.render()

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(LottoResult.objects.count(), 1)
