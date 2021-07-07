from cardtel.models import (
    Game,
    Player,
    Table,
)
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
