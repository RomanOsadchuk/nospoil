from rest_framework import serializers
from nospoil.constants import MAX_PLAYOFF_ROUNDS
from .models import Playoff
from .services import create_matches, update_matches


# different serializers because rounds and double filds are needed to create,
# but they should not be changed when editing,
# also grid is needed to displaying one playoff, but not list

class PlayoffListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    rounds = serializers.IntegerField(min_value=2, max_value=MAX_PLAYOFF_ROUNDS)

    class Meta:
        model = Playoff
        fields = ('url', 'id', 'title', 'sport', 'double', 'rounds',
                  'owner', 'private')

    def create(self, validated_data):
        playoff = Playoff.objects.create(**validated_data)
        # the logic is more complex than nested serialization
        create_matches(playoff, self.initial_data.get('matches', {}))
        return playoff


class PlayoffDetailSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    grid = serializers.ReadOnlyField()

    class Meta:
        model = Playoff
        fields = ('url', 'id', 'title', 'sport', 'owner', 'private', 'grid')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.sport = validated_data.get('sport', instance.sport)
        instance.private = validated_data.get('private', instance.private)
        instance.save()
        # the logic is more complex than nested serialization
        update_matches(instance, self.initial_data.get('matches', {}))
        return instance
