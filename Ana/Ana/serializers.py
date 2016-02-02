from rest_framework import serializers
from Ana.models import BetTicket
from django.contrib.auth.models import User


class BetTicketSerializer(serializers.HyperlinkedModelSerializer):
    """
    Manages the serialization over BetTicket objects
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = BetTicket
        fields = ('url', 'created_at', 'bet', 'lotto_id', 'owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Manages the serialization over User objects
    """
    bets = serializers.HyperlinkedRelatedField(queryset=BetTicket.objects.all(), view_name='betticket-detail',
                                               many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'bets')
