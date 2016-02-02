from rest_framework import viewsets, permissions, renderers, status, mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from Bob.models import LottoResult
from Bob.serializers import LottoResultSerializer


class LottoResultViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Manages the operations over Lotto Result abstraction
    """
    queryset = LottoResult.objects.all()
    serializer_class = LottoResultSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @list_route(renderer_classes=(renderers.JSONRenderer, ))
    def next_lotto(self, request, *args, **kwargs):
        """
        Returns the next Lotto identifier (LottoResult.id) to be consumed be client APIs
        :param request: the client request object
        :param args: extra unnamed arguments
        :param kwargs: extra named arguments
        :return: JSON Response with next LottoResult identifier at 'next' field
        """
        if request.method == 'GET':
            last_lotto = self.get_queryset().last()
            return Response(data={'next': '{}'.format(last_lotto.id + 1 if last_lotto else 1)})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @detail_route(renderer_classes=(renderers.JSONRenderer, ))
    def matches_winner(self, request, *args, **kwargs):
        """
        Given a bet (query string parameter) it provides information if is a winner ticket
        :param request: the client request object
        :param args: extra unnamed arguments
        :param kwargs: extra named arguments
        :return: JSON Response with boolean information at 'matches' field about the winner ticket
        """
        if request.method == 'GET':
            bet = request.query_params.get('bet')
            if bet and len(bet.split(' ')) == 6:
                lotto_result = self.get_object()
                result = lotto_result.result.split(' ')
                for element in bet.split(' '):
                    if element in result:
                        result.remove(element)
                if not result:
                    return Response(data={'matches': True})
                else:
                    return Response(data={'matches': False})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

