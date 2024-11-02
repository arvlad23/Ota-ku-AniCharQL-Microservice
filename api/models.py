import uuid

from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
import logging
from django.utils import timezone
logger = logging.getLogger(__name__)

class AnimeKindEnum(models.TextChoices):
    tv = 'tv',
    movie = 'movie',
    ova = 'ova',
    ona = 'ona',
    special = 'special',
    tv_special = 'tv_special',
    music = 'music',
    pv = 'pv',
    cm = 'cm'
class AnimeRatingEnum(models.TextChoices):
    NONE = "none",
    G = 'g',
    PG = "pg",
    PG_13 = "pg_13",
    R_17 = "r",
    R_PLUS = "r_plus"
    RX = "rx"
class StatusEnum(models.TextChoices):
    ANONS = 'Planned',
    ONGOING = 'Airing',
    RELEASED = 'released',

class IncompleteData(models.Model):
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.day} - {self.month} - {self.year}"
    @property
    def date(self):
        return f"{self.year}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}"

class Poster(models.Model):
    main2xUrl = models.URLField(null=True, blank=True)
    mainAlt2xUrl = models.URLField(null=True, blank=True)
    mainAltUrl = models.URLField(null=True, blank=True)
    mainUrl = models.URLField(null=True, blank=True)
    mini2xUrl = models.URLField(null=True, blank=True)
    miniAlt2xUrl = models.URLField(null=True, blank=True)
    miniAltUrl = models.URLField(null=True, blank=True)
    miniUrl = models.URLField(null=True, blank=True)
    originalUrl = models.URLField(null=True, blank=True)
    preview2xUrl = models.URLField(null=True, blank=True)
    previewAlt2xUrl = models.URLField(null=True, blank=True)
    previewAltUrl = models.URLField(null=True, blank=True)
    previewUrl = models.URLField(null=True, blank=True)

class GenreEntryTypeEnum(models.TextChoices):
    ANIME = "Anime",
    MANGA = 'Mange'

class GenreKindEnum(models.TextChoices):
    DEMOGRAPHIC = 'demographic',
    GENRE = 'genre',
    THEME = 'theme'

class Genre(models.Model):
    entryType = models.CharField(choices=GenreEntryTypeEnum, max_length=5, null=True, blank=True)
    kind = models.CharField(choices=GenreKindEnum, max_length=12, null=True, blank=True)
    name = models.CharField(max_length=120)
    russian = models.TextField(null=True, blank=True)

class Studio(models.Model):
    imageUrl = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)

class ExternalLinkKindEnum(models.TextChoices):
    ANIDB = 'anime_db', 'AniDB'
    OFFICIAL_SITE = 'official_site', 'Official Site'
    WIKIPEDIA = 'wikipedia', 'Wikipedia'
    ANIME_NEWS_NETWORK = 'anime_news_network', 'Anime News Network'
    MYANIMELIST = 'myanimelist', 'MyAnimeList'
    WORLD_ART = 'world_art', 'World Art'
    KINOPOISK = 'kinopoisk', 'KinoPoisk'
    KAGE_PROJECT = 'kage_project', 'Kage Project'
    TWITTER = 'twitter', 'Twitter/X'
    SMOTRET_ANIME = 'smotret_anime', 'Anime 365'
    CRUNCHYROLL = 'crunchyroll', 'Crunchyroll'
    AMAZON = 'amazon', 'Amazon'
    HIDIVE = 'hidive', 'Hidive'
    HULU = 'hulu', 'Hulu'
    IVI = 'ivi', 'Ivi'
    KINOPOISK_HD = 'kinopoisk_hd', 'KinoPoisk HD'
    WINK = 'wink', 'Wink'
    NETFLIX = 'netflix', 'Netflix'
    OKKO = 'okko', 'Okko'
    YOUTUBE = 'youtube', 'Youtube'
    READMANGA = 'readmanga', 'ReadManga'
    MANGALIB = 'mangalib', 'MangaLib'
    REMANGA = 'remanga', 'ReManga'
    MANGAPDATES = 'mangaupdates', 'Baka-Updates'
    MANGADEX = 'mangadex', 'MangaDex'
    MANGAFOX = 'mangafox', 'MangaFox'
    MANGACHAN = 'mangachan', 'Mangachan'
    MANGAHUB = 'mangahub', 'Mangahub'
    NOVEL_TL = 'novel_tl', 'Novel.tl'
    RURANOBE = 'ruranobe', 'RuRanobe'
    RANOBELIB = 'ranobelib', 'RanobeLib'
    NOVELUPDATES = 'novelupdates', 'Novel Updates'

class ExternalLink(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    url = models.URLField(null=True, blank=True)
    kind = models.CharField(choices=ExternalLinkKindEnum, max_length=18, null=True, blank=True)

class Topic(models.Model):
    body = models.TextField(null=True, blank=True)
    commentsCount = models.IntegerField(null=True, blank=True)
    createdAt = models.DateTimeField(null=True, blank=True)
    updatedAt = models.DateTimeField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    htmlBody = models.TextField(null=True, blank=True)
    tags = ArrayField(models.TextField(), null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True)
    type = models.CharField(max_length=120, null=True, blank=True)

class Character(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    descriptionHtml = models.TextField(null=True, blank=True)
    descriptionSource = models.TextField(null=True, blank=True)
    isAnime = models.BooleanField(default=False)
    isManga = models.BooleanField(default=False)
    isRanobe = models.BooleanField(default=False)
    japanese = models.TextField(null=True, blank=True)
    malId = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=120)
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE, null=True, blank=True)
    russian = models.TextField(null=True, blank=True)
    synonyms = ArrayField(models.TextField(), null=True, blank=True, default=list),
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.malId = self.id
        super().save(update_fields=['malId'])

class CharacterRole(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    rolesEn = ArrayField(models.TextField(), null=True, blank=True)
    rolesRu = ArrayField(models.TextField(), null=True, blank=True)

class Person(models.Model):
    birthOn = models.ForeignKey(IncompleteData, on_delete=models.CASCADE, related_name="person_birthOn", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    deceasedOn = models.ForeignKey(IncompleteData, on_delete=models.CASCADE, related_name="person_decasedOn", null=True, blank=True)
    isMangaka = models.BooleanField(default=False)
    isProducer = models.BooleanField(default=False)
    isSeyu = models.BooleanField(default=False)
    japanese = models.TextField(null=True, blank=True)
    malId = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=120)
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE, null=True, blank=True)
    russian = models.TextField(null=True, blank=True)
    synonyms = ArrayField(models.TextField(), null=True, blank=True, default=list),
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)

class PersonRole(models.Model):
    rolesEn = ArrayField(models.TextField(), null=True, blank=True)
    rolesRu = ArrayField(models.TextField(), null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

class RelationKindEnum(models.TextChoices):
    ADAPTATION = 'adaptation', 'Adaptation'
    ALTERNATIVE_SETTING = 'alternative_setting', 'Alternative Setting'
    ALTERNATIVE_VERSION = 'alternative_version', 'Alternative Version'
    CHARACTER = 'character', 'Character'
    FULL_STORY = 'full_story', 'Full Story'
    OTHER = 'other', 'Other'
    PARENT_STORY = 'parent_story', 'Parent Story'
    PREQUEL = 'prequel', 'Prequel'
    SEQUEL = 'sequel', 'Sequel'
    SIDE_STORY = 'side_story', 'Side Story'
    SPIN_OFF = 'spin_off', 'Spin-off'
    SUMMARY = 'summary', 'Summary'

class Manga(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
class Related(models.Model):
    relationText = models.TextField(null=True, blank=True)
    relationEn = models.CharField(max_length=255, null=True, blank=True)
    anime = models.ForeignKey("Anime", on_delete=models.CASCADE, null=True, related_name='related_anime', blank=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, null=True, related_name='related_manga', blank=True)
    relationKind = models.CharField(choices=RelationKindEnum, max_length=19, null=True, blank=True)

class VideoKindEnum(models.TextChoices):
    PV = 'pv', 'PV'
    CHARACTER_TRAILER = 'character_trailer', 'Character trailer'
    CM = 'cm', 'CM'
    OP = 'op', 'OP'
    ED = 'ed', 'ED'
    OP_ED_CLIP = 'op_ed_clip', 'Music'
    CLIP = 'clip', 'Clip'
    OTHER = 'other', 'Other'
    EPISODE_PREVIEW = 'episode_preview', 'Episode preview'

class Video(models.Model):
    imageUrl = models.URLField(null=True, blank=True)
    kind = models.CharField(choices=VideoKindEnum, max_length=20, null=True, blank=True)
    name = models.CharField(max_length=120)
    playerUrl = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

class Screenshot(models.Model):
    originalUrl = models.URLField(null=True, blank=True)
    x166Url = models.URLField(null=True, blank=True)
    x332Url = models.URLField(null=True, blank=True)

class ScoresStat(models.Model):
    score = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
class UserRateStatusEnum(models.TextChoices):
    PLANNED = 'planned', 'Planned to Watch'
    WATCHING = 'watching', 'Watching'
    REWATCHING = 'rewatching', 'Rewatching'
    COMPLETED = 'completed', 'Completed'
    ON_HOLD = 'on_hold', 'On Hold'
    DROPPED = 'dropped', 'Dropped'
class StatusesStat(models.Model):
    count = models.IntegerField(default=0)
    status = models.CharField(choices=UserRateStatusEnum, max_length=20, null=True, blank=True)

class Anime(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    malId = models.IntegerField(null=True)
    russian = models.TextField(null=True, blank=True)
    english = models.TextField(null=True, blank=True)
    japanese = models.TextField(null=True, blank=True)
    licenseNameRu = models.TextField(max_length=255, null=True, blank=True)
    synonyms = ArrayField(models.TextField(max_length=255, null=True, blank=True),default=list, null=True)
    kind = models.CharField(choices=AnimeKindEnum.choices, max_length=10)
    rating = models.CharField(choices=AnimeRatingEnum, max_length=10, null=True)
    score = models.FloatField(null=True)
    status = models.CharField(choices=StatusEnum, max_length=10, null=True)
    episodes = models.PositiveIntegerField(default=0, blank=True)
    episodesAired = models.PositiveIntegerField(default=0, blank=True)
    duration = models.PositiveIntegerField(default=0, blank=True)
    airedOn = models.ForeignKey(IncompleteData, on_delete=models.CASCADE, null=True, related_name='airedOn', blank=True)
    releasedOn = models.ForeignKey(IncompleteData, on_delete=models.CASCADE, null=True, related_name='releasedOn', blank=True)
    url = models.URLField(null=True, blank=True)
    season = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE, null=True, related_name='poster', blank=True)
    fansubbers = ArrayField(models.TextField(max_length=255, null=True, blank=True),default=list, null=True)
    fandubbers = ArrayField(models.TextField(max_length=255, null=True, blank=True),default=list, null=True)
    licensors = ArrayField(models.TextField(max_length=255, null=True, blank=True),default=list, null=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    nextEpisodeAt = models.CharField(max_length=255, null=True, blank=True)
    isCensored = models.BooleanField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, default=dict, blank=True)
    studios = models.ManyToManyField(Studio, default=dict, blank=True)
    externalLinks = models.ManyToManyField(ExternalLink, default=dict, blank=True)
    characterRoles = models.ManyToManyField(CharacterRole, default=dict, blank=True)
    personRoles = models.ManyToManyField(PersonRole, default=dict, blank=True)
    related = models.ManyToManyField(Related, default=dict, blank=True, related_name="anime_related")
    videos = models.ManyToManyField(Video, default=dict, blank=True)
    screenshots = models.ManyToManyField(Screenshot, default=dict, blank=True)
    scoresStats = models.ManyToManyField(ScoresStat, default=dict, blank=True)
    statusesStats = models.ManyToManyField(StatusesStat, default=dict, blank=True)
    description = models.TextField(null=True, blank=True)
    descriptionHtml = models.TextField(null=True, blank=True)
    descriptionSource = models.TextField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.mal_id = self.id

        super(Anime, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.name)

