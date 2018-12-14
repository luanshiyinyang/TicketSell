from rest_framework import serializers
from apps.ticketsale.models import Tickets


class TicketsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tickets
        fields = ('url', 'id', 'num', 'name_start', 'name_end', 'date', 'time', 'brief', 'seats',)