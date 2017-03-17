from rest_framework import serializers
from nospoil.constants import MAX_PLAYOFF_ROUNDS
from .models import Playoff
from .services import create_matches, update_matches


class PlayoffListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    rounds = serializers.IntegerField(min_value=2, max_value=MAX_PLAYOFF_ROUNDS)

    class Meta:
        model = Playoff
        fields = ('id', 'title', 'sport', 'double', 'rounds',
                  'owner', 'private')

    def create(self, validated_data):
        playoff = Playoff.objects.create(**validated_data)
        matches = self.initial_data.get('matches', {})
        create_matches(playoff, matches)
        return playoff


class PlayoffDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    grid = serializers.ReadOnlyField()

    class Meta:
        model = Playoff
        fields = ('id', 'title', 'sport', 'owner', 'private', 'grid')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.sport = validated_data.get('sport', instance.sport)
        instance.private = validated_data.get('private', instance.private)
        instance.save()
        matches = self.initial_data.get('matches', {})
        update_matches(instance, matches)
        return instance
