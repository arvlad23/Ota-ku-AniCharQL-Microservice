import graphene
from graphene_django.types import DjangoObjectType
from .models import Anime, ExternalLink
from datetime import date
import json

class PosterType(graphene.ObjectType):
    id = graphene.ID()
    original_url = graphene.String()
    main_url = graphene.String()
class DateType(graphene.ObjectType):
    year = graphene.Int()
    month = graphene.Int()
    day = graphene.Int()
    date = graphene.String()

    @staticmethod
    def resolve_year(root, info):
        return root.year

    @staticmethod
    def resolve_month(root, info):
        return root.month

    @staticmethod
    def resolve_day(root, info):
        return root.day

    @staticmethod
    def resolve_date(root, info):
        return root.isoformat()  # Формат даты в виде строки YYYY-MM-DD

class GenreType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    russian = graphene.String()
    kind = graphene.String()

class StudiosType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    imageUrl = graphene.String()
class PosterType(graphene.ObjectType):
    id = graphene.ID()
    originalUrl = graphene.String()  # Предположим, у вас есть это поле
    mainUrl = graphene.String()       # Предположим, у вас есть это поле

class PersonType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    poster = graphene.Field(PosterType)  # Изменено на конкретный тип

class RolesType(graphene.ObjectType):
    id = graphene.ID()
    rolesRu = graphene.List(graphene.String)
    rolesEn = graphene.List(graphene.String)
class PersonRoleType(RolesType):
    person = graphene.Field(PersonType)

class CharacterRoleType(RolesType):
    character = graphene.List(PersonType)

class RelatedItemType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

class RelatedType(graphene.ObjectType):
    id = graphene.ID()
    anime = graphene.Field(RelatedItemType)
    manga = graphene.Field(RelatedItemType)
    relationKind = graphene.String()
    relationText = graphene.String()

class VideoType(graphene.ObjectType):
    id = graphene.ID()
    url = graphene.String()
    name = graphene.String()
    kind = graphene.String()
    playerUrl = graphene.String()
    imageUrl = graphene.String()

class ScreenshotType(graphene.ObjectType):
    id = graphene.ID()
    originalUrl = graphene.String()
    x166Url = graphene.String()
    x332Url = graphene.String()

class ScoresStatsType(graphene.ObjectType):
    score = graphene.Float()
    count = graphene.Int()

class StatusesStatsType(graphene.ObjectType):
    status = graphene.String()
    count = graphene.Int()

class ExternalLinksType(DjangoObjectType):
    class Meta:
        model = ExternalLink
        fields = '__all__'
class AnimeType(DjangoObjectType):
    aired_on = graphene.Field(DateType)
    released_on = graphene.Field(DateType)
    poster = graphene.Field(PosterType)
    genres = graphene.List(GenreType)
    studios = graphene.List(StudiosType)
    personRoles = graphene.List(PersonRoleType)
    characterRoles = graphene.List(CharacterRoleType)
    related = graphene.List(RelatedType)
    videos = graphene.List(VideoType)
    screenshots = graphene.List(ScreenshotType)
    scoresStats = graphene.List(ScoresStatsType)
    statusesStats = graphene.List(StatusesStatsType)

    class Meta:
        model = Anime
        fields = "__all__"

    def resolve_aired_on(self, info):
        return self.aired_on if self.aired_on else date.min  # передаём дату в DateType

    def resolve_released_on(self, info):
        return self.released_on if self.released_on else date.min

    def resolve_poster(self, info):
        if self.poster:
            return {
                "id": self.id,
                "original_url": self.poster.get('original_url'),
                "main_url" : self.poster.get('main_url')
            }
        return None

    def resolve_genres(self, info):
        return json.loads(self.genres)

    def resolve_studios(self, info):
        return json.loads(self.studios)

    def resolve_person_roles(self, info):
        roles = json.loads(self.person_roles)  # Преобразуем JSON в объекты Python
        return [PersonRoleType(**role) for role in roles]  # Возвращаем список ролей

    def resolve_character_roles(self, info):
        characters = json.loads(self.character_roles)
        return [PersonRoleType(**character) for character in characters]

    def resolve_related(self, info):
        relateds = json.loads((self.related))
        return [RelatedType(**related) for related in relateds]



class Query(graphene.ObjectType):
    animes = graphene.List(
        AnimeType,
        search=graphene.String(),
        limit=graphene.Int(),
        kind=graphene.String()
    )

    def resolve_animes(self, info, search=None, limit=None, kind=None, **kwargs):
        qs = Anime.objects.all()
        if search:
            qs = qs.filter(name__icontains=search)
        if kind and kind != "!special":
            qs = qs.exclude(kind="special")
        if limit:
            qs = qs[:limit]
        return qs





schema = graphene.Schema(query=Query)
