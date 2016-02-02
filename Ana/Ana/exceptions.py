from rest_framework.exceptions import APIException


class BobServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'The service of Lotto is temporarily unavailable, please try again later.'


class BobServiceLottoWithoutResult(APIException):
    status_code = 404
    default_detail = 'The result of the request Lotto is not available yet.'
