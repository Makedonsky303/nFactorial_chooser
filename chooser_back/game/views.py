from rest_framework import generics,status
from .models import Game, Participant
from .serializers import GameSerializer, ParticipantSerializer
from rest_framework.response import Response
import random

class GameCreateView(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        participants_data = request.data.pop('participants', [])
        winner_data = request.data.pop('winner', None)  

        
        created_participants = []
        for pdata in participants_data:
            pdata.pop('id', None)  # Убираем id, если он есть
            participant = Participant.objects.create(**pdata)
            created_participants.append(participant)

        game = Game.objects.create(**request.data)

    
        game.participants.set(created_participants)

        serializer = self.get_serializer(game)
        
        return Response({"game_id": game.id}, status=status.HTTP_201_CREATED)
    
class PickParticipantView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            participants = Participant.objects.all()
            if not participants.exists():
                return Response({"error": "No participants left"}, status=status.HTTP_400_BAD_REQUEST)

            participant = random.choice(participants)
            participant_data = {
                "id": participant.id,
                "color": participant.color
            }
            participant.delete() 

            return Response(participant_data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Ошибка выбора участника:", e)
            return Response({"error": "Ошибка выбора участника"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ParticipantListView(generics.ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    
class ResetParticipantsView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id')
        if not game_id:
            return Response({"error": "Не указан ID игры"}, status=status.HTTP_400_BAD_REQUEST)

        Participant.objects.filter(game_id=game_id).delete()
        return Response({"message": f"Все участники игры {game_id} удалены"}, status=status.HTTP_200_OK)

    

class AssignTaskView(generics.GenericAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    TASKS = [
        "100 отжиманий",
        "100 приседаний",
        "100 пресс",
        "10км бега",
        "Пройти nFactorial на грант",
    ]

    def post(self, request, participant_id, *args, **kwargs):
        participant = self.get_queryset().filter(id=participant_id).first()
        if not participant:
            return Response({"detail": "Участник не найден"}, status=status.HTTP_404_NOT_FOUND)

        task = random.choice(self.TASKS)
        participant.task = task
        participant.save()

        return Response({"task": task})
    
class RemoveParticipantView(generics.GenericAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def post(self, request, participant_id, *args, **kwargs):
        participant = self.get_queryset().filter(id=participant_id).first()
        if participant:
            participant.delete()
            return Response({"message": "Участник удалён"})
        return Response({"detail": "Участник не найден"}, status=status.HTTP_404_NOT_FOUND)

class CompleteTaskView(generics.GenericAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def post(self, request, participant_id, *args, **kwargs):
        participant = self.get_queryset().filter(id=participant_id).first()
        if not participant:
            return Response({"detail": "Участник не найден"}, status=status.HTTP_404_NOT_FOUND)

        participant.task = None
        participant.save()
        return Response({"message": "Задание завершено"})
    
class GameDeleteView(generics.DestroyAPIView):
    queryset = Game.objects.all()

    def delete(self, request, *args, **kwargs):
        game_id = kwargs.get('pk')
        try:
            game = Game.objects.get(id=game_id)
            game.delete()
            return Response({"message": "Игра удалена"}, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({"error": "Игра не найдена"}, status=status.HTTP_404_NOT_FOUND)