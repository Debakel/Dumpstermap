from __future__ import unicode_literals

import json

from django.contrib.gis.db import models
from django.utils import timezone
from geojson import Feature


class Dumpster(models.Model):
    location = models.PointField()
    created = models.DateTimeField(auto_created=True)

    imported = models.BooleanField(default=False)
    imported_from = models.CharField(max_length=255, null=True, blank=True)
    import_reference = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(max_length=255, null=True, default="Dumpster")

    @property
    def rating(self):
        return self.good - self.bad

    @property
    def good(self):
        return self.voting_set.filter(value=VotingValue.GOOD).count()

    @property
    def bad(self):
        return self.voting_set.filter(value=VotingValue.BAD).count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Dumpster, self).save(*args, **kwargs)

    @property
    def __geo_interface__(self) -> Feature:
        return Feature.to_instance(
            {
                "type": "Feature",
                "geometry": json.loads(self.location.json),
                "properties": {"id": self.id, "name": self.name},
            }
        )


class VotingValue(models.TextChoices):
    """Possible ratings a voting can give a dumpster."""

    GOOD = "good", "Good"
    BAD = "senseless", "Not good"
    NEUTRAL = "average", "Neutral"


class Voting(models.Model):
    dumpster = models.ForeignKey(Dumpster, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, choices=VotingValue.choices)
    created_date = models.DateTimeField()
    comment = models.CharField(max_length=2000)

    @property
    def name(self):
        return "Anonymous"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        return super(Voting, self).save(*args, **kwargs)
