from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cardtel.models import (
    Game,
    Player,
    Table,
)

from cardtel.api.v1.serializers import GameSerializer


class GameListView(APIView):
    """
    Game ListView
    """

    # queryset = Game.objects.all()
    # serializer_class = GameSerializer

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
