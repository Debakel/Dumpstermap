from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils import timezone


class Dumpster(models.Model):
    location = models.PointField()
    created = models.DateTimeField(auto_created=True)

    imported = models.BooleanField(default=False)
    imported_from = models.CharField(max_length=255, null=True, blank=True)
    import_reference = models.CharField(max_length=255, null=True, blank=True)

    @property
    def name(self):
        return "Netto"

    @property
    def rating(self):
        return self.good - self.bad

    @property
    def good(self):
        return self.voting_set.filter(value=Voting.GOOD).count()

    @property
    def bad(self):
        return self.voting_set.filter(value=Voting.BAD).count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Dumpster, self).save(*args, **kwargs)


class Voting(models.Model):
    dumpster = models.ForeignKey(Dumpster)
    GOOD = 'good'
    BAD = 'senseless'
    NEUTRAL = 'average'
    VOTING_CHOICES = ((GOOD, 'Good'),
                      (BAD, 'Not good'),
                      (NEUTRAL, 'Neutral'))  # todo
    value = models.CharField(max_length=255, choices=VOTING_CHOICES)
    created_date = models.DateTimeField()
    comment = models.CharField(max_length=2000)
    #todo: session

    @property
    def name(self):
        return 'Gerd'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        return super(Voting, self).save(*args, **kwargs)

