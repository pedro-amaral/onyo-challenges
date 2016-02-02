from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, renderers, status, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from Ana.models import BetTicket
from Ana.permissions import IsOwner
from Ana.serializers import BetTicketSerializer, UserSerializer
from Ana.utils import BobHelper
from Ana.exceptions import BobServiceLottoWithoutResult, BobServiceUnavailable


class BetTicketViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    Manages the operations over Bet Ticket abstraction
    """
    queryset = BetTicket.objects.all()
    serializer_class = BetTicketSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner, )

    @detail_route(renderer_classes=(renderers.JSONRenderer, renderers.StaticHTMLRenderer))
    def is_a_winner(self, request, *args, **kwargs):
        """
        Given a ticket it requests to Bob to check if is a winner of the related lotto
        :param request: the client request object
        :param args: extra unnamed arguments
        :param kwargs: extra named arguments
        :return: boolean indicating if is a winner or a string with error message
        """
        if request.method == 'GET':
            bet_ticket = self.get_object()
            try:
                result = BobHelper.is_a_winner_ticket(bet_ticket.id, bet_ticket.lotto_id, bet_ticket.bet)
            except BobServiceLottoWithoutResult as error:
                result = str(error)
            return Response(data=result)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer: BetTicketSerializer):
        # Request to know the next lotto
        next_lotto_id = BobHelper.check_next_lotto()
        serializer.save(owner=self.request.user, lotto_id=next_lotto_id)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
