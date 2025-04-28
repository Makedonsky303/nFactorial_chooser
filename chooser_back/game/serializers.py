from rest_framework import serializers
from .models import Game, Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class GameCreateSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    winner = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Game
        fields = "__all__"

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        game = Game.objects.create(**validated_data)
        participants = []

        for participant_data in participants_data:
            participant = Participant.objects.create(**participant_data)
            participants.append(participant)

        game.participants.set(participants)
        return game

class GameSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    winner = ParticipantSerializer()

    class Meta:
        model = Game
        fields = "__all__"
