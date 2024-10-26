from django.db import models
from django.utils import timezone


class ExternalLink(models.Model):
    kind = models.CharField(max_length=50)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.kind}: {self.url}'
class Anime(models.Model):
    mal_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)
    russian = models.CharField(max_length=200, null=True, blank=True)
    license_name_ru = models.CharField(max_length=200, null=True, blank=True)
    english = models.CharField(max_length=200, null=True, blank=True)
    japanese = models.CharField(max_length=200, null=True, blank=True)
    synonyms = models.JSONField(default=list, blank=True)
    kind = models.CharField(max_length=50)
    rating = models.CharField(max_length=10, null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50)
    episodes = models.IntegerField(null=True, blank=True)
    episodes_aired = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    aired_on = models.DateField(null=True, blank=True)
    released_on = models.DateField(null=True, blank=True)
    url = models.URLField(max_length=200)
    season = models.CharField(max_length=20, null=True, blank=True)
    poster = models.JSONField(null=True, blank=True)
    fansubbers = models.JSONField(default=list, blank=True)
    fandubbers = models.JSONField(default=list, blank=True)
    licensors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    next_episode_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    isCensored = models.BooleanField(default=False)
    genres = models.JSONField(default=list, blank=True)
    studios = models.JSONField(default=list, blank=True)
    external_links = models.ManyToManyField(ExternalLink, blank=True, related_name='animes')
    person_roles = models.JSONField(default=list, blank=True)
    character_roles = models.JSONField(default=list, blank=True)
    related = models.JSONField(default=list, blank=True)
    videos = models.JSONField(default=list, blank=True)
    screenshots = models.JSONField(default=list, blank=True)
    scores_stats = models.JSONField(default=list, blank=True)
    statusesStats = models.JSONField(default=list, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    descriptionHtml = models.TextField(null=True, blank=True)
    descriptionSource = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
