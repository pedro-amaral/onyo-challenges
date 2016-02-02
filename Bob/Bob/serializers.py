from rest_framework import serializers
from Bob.models import LottoResult


class LottoResultSerializer(serializers.ModelSerializer):
    """
    Manages the serialization over LottoResult objects
    """
    class Meta:
        model = LottoResult
        fields = '__all__'

