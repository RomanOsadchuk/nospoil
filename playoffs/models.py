from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .helpers import get_grid, slugify


class Playoff(models.Model):
    sport = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    double = models.BooleanField(default=True)  # double or single elimination
    rounds = models.PositiveSmallIntegerField(default=5)
    private = models.BooleanField(default=False)  # only owner can edit
    owner = models.ForeignKey(User, null=True, related_name='playoffs',
                              on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-last_modified']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.owner:
            self.private = False
        super(Playoff, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'pk': self.pk, 'slug': self.slug}
        return reverse('playoffs:detail', kwargs=kwargs)

    @property
    def grid(self):
        # grid explained in helpers.get_grid function
        values = ('position', 'side_a', 'side_b', 'winner_a', 'youtube_id')
        matches = list(self.matches.order_by('position').values(*values))
        return get_grid(matches, self.rounds, self.double)

    def __unicode__(self):
        return self.title


class Match(models.Model):
    playoff = models.ForeignKey(Playoff, related_name='matches',
                                on_delete=models.CASCADE)
    # position explained in helpers.get_match_positions
    position = models.CharField(max_length=8)
    side_a = models.CharField(max_length=32, blank=True)  # side: team/player
    side_b = models.CharField(max_length=32, blank=True)
    winner_a = models.NullBooleanField()
    youtube_id = models.CharField(max_length=32, blank=True)

    class Meta:
        unique_together = (('playoff', 'position'),)

    def __unicode__(self):
        return '{}: {} - {}'.format(self.position, self.side_a, self.side_b)
