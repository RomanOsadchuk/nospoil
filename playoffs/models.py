from __future__ import unicode_literals
from re import sub
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Playoff(models.Model):
    sport = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    double = models.BooleanField(default=True)  # double or single elimination
    rounds = models.PositiveSmallIntegerField(default=5)
    private = models.BooleanField(default=False)  # only owner can edit
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-last_modified']

    def save(self, *args, **kwargs):
        title = self.title or '-----'
        self.slug = sub(r'[^\w]+', '-', title)
        super(Playoff, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'pk': self.pk, 'slug': self.slug}
        return reverse('playoffs:detail', kwargs=kwargs)

    def __unicode__(self):
        return self.title


class Match(models.Model):
    playoff = models.ForeignKey(Playoff, on_delete=models.CASCADE)
    position = models.CharField(max_length=8)  # todo - explain position
    side_a = models.CharField(max_length=32, blank=True)  # side: team/player
    side_b = models.CharField(max_length=32, blank=True)
    winner_a = models.NullBooleanField()
    youtube_id = models.CharField(max_length=32, blank=True)

    class Meta:
        unique_together = (('playoff', 'position'),)

    @property
    def embed_yt_src(self):
        if not self.youtube_id:
            return ''
        sep = '&' if '?' in self.youtube_id else '?'
        dom = 'https://www.youtube.com/embed/'
        return dom + self.youtube_id + sep + 'controls=0'

    def __unicode__(self):
        return '{}: {} - {}'.format(self.position, self.side_a, self.side_b)
