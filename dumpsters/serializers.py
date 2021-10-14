from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Dumpster, Voting


class VotingSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True, allow_null=True)

    class Meta:
        model = Voting
        fields = ("id", "value", "comment", "created_date", "dumpster", "name")


class NestedVotingSerializer(VotingSerializer):
    class Meta:
        model = Voting
        fields = ("id", "value", "comment", "created_date", "name")


class DumpsterSerializer(GeoFeatureModelSerializer):
    voting_set = NestedVotingSerializer(many=True)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        votings_data = validated_data.pop("voting_set")
        dumpster = Dumpster.objects.create(**validated_data)
        for voting_data in votings_data:
            Voting.objects.create(dumpster=dumpster, **voting_data)
        return dumpster

    class Meta:
        model = Dumpster
        geo_field = "location"
        fields = ("id", "name", "created", "rating", "good", "bad", "voting_set")
