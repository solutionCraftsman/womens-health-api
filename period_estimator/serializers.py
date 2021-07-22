from rest_framework import serializers
from .models import CreateCycleRequest, PeriodCycle


class CreateCycleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CreateCycleRequest
        fields = '__all__'

