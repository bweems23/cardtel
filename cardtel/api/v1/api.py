from rest_framework.views import APIView
from rest_framework.response import Response

from cardtel.models import (
    Game,
)

from cardtel.api.v1.serializers import GameSerializer


class GameListView(APIView):
    """
    Game ListView
    """
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
