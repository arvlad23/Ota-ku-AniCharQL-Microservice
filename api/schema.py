import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from graphql.error.graphql_error import GraphQLError
from graphql.language import ast
from .models import Anime, IncompleteData, Poster, Genre, Studio, ExternalLink, CharacterRole, Character, PersonRole, \
    Person, Related, Manga, Video, Screenshot, ScoresStat, StatusesStat, AnimeRatingEnum


class IncompleteDataType(DjangoObjectType):
    date = graphene.String()
    class Meta:
        model = IncompleteData

class PosterType(DjangoObjectType):
    class Meta:
        model = Poster

class GenresType(DjangoObjectType):
    class Meta:
        model = Genre

class StudiosType(DjangoObjectType):
    class Meta:
        model = Studio

class ExternalLinkType(DjangoObjectType):
    class Meta:
        model = ExternalLink
class CharacterType(DjangoObjectType):
    class Meta:
        model = Character

class PersonType(DjangoObjectType):
    class Meta:
        model = Person
class PersonRolesType(DjangoObjectType):
    class Meta:
        model = PersonRole
class CharacterRolesType(DjangoObjectType):
    class Meta:
        model = CharacterRole
class MangaType(DjangoObjectType):
    class Meta:
        model = Manga
class RelatedType(DjangoObjectType):
    class Meta:
        model = Related
class VideoType(DjangoObjectType):
    kind = graphene.String()
    class Meta:
        model = Video

class ScreenshotType(DjangoObjectType):
    class Meta:
        model = Screenshot

class ScoresStatType(DjangoObjectType):
    class Meta:
        model = ScoresStat
class StatusesStatType(DjangoObjectType):
    status = graphene.String()
    class Meta:
        model = StatusesStat
class AnimeType(DjangoObjectType):
    synonyms = graphene.List(graphene.String)
    status = graphene.String()
    rating = graphene.String()
    kind = graphene.String()
    fansubbers = graphene.List(graphene.String)
    fandubbers = graphene.List(graphene.String)
    licensors = graphene.List(graphene.String)
    createdAt = graphene.DateTime()
    updatedAt = graphene.DateTime()
    class Meta:
        model = Anime

    def resolve_synonyms(self, info):
        return self.synonyms if self.synonyms is not None else []

class OrderEnum(graphene.Enum):
    ID = "id"
    ID_DESC = "-id"
    RANKED = "score"
    KIND = "kind"
    POPULARITY = "score"
    NAME = "name"
    AIRED_ON = "airedOn__date"
    EPISODES = "episodes"
    STATUS = "status"
    RANDOM = "random"
    RANKED_RANDOM = "ranked_random"
    RANKED_SHIKI = "ranked_shiki"
    CREATED_AT = "createdAt"
    CREATED_AT_DESC = "-createdAt"

class AnimeKindString(graphene.String):
    """
    List of values separated by comma. Add ! before value to apply negative filter.
    movie - Movies
    music - Music
    ona - ONA
    ova/ona - OVA/ONA
    ova - OVA
    special - Specials
    tv - TV Series
    tv_13 - Short TV Series
    tv_24 - Average TV Series
    tv_48 - Long TV Series
    tv_special - TV Specials
    pv - Promotional Videos
    cm - Commercial Messages
    """

    @classmethod
    def serialize(cls, value):
        return value

    @classmethod
    def parse_value(cls, value):
        if not isinstance(value, str):
            raise ValueError("Expected a string value.")
        return value

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValueNode):  # Убедитесь, что вы используете StringValueNode
            return node.value
        return None

class SeasonString(AnimeKindString):
    """
    List of values separated by comma. Add ! before value to apply negative filter.
    Examples:
    summer_2017
    2016
    2014_2016
    199x
    """
    pass

class StatusString(AnimeKindString):
    """
    List of values separated by comma. Add ! before value to apply negative filter.
    anons - Planned
    ongoing - Airing
    released - Released
    """

class DurationString(graphene.Scalar):
    """
    List of values separated by comma. Add ! before value to apply negative filter.
    S - Less than 10 minutes
    D - Less than 30 minutes
    F - More than 30 minutes
    """

class RatingString(AnimeKindString):
    """
    List of values separated by comma. Add ! before value to apply negative filter.
    none - No rating
    g - G - All ages
    pg - PG - Children
    pg_13 - PG-13 - Teens 13 or older
    r - R - 17+ recommended (violence & profanity)
    r_plus - R+ - Mild Nudity (may also contain violence & profanity)
    rx - Rx - Hentai (extreme sexual content/nudity)
    """
def filter_by_field(queryset, field_name, values):
    filters = values.split(',')
    include_filters = Q()
    exclude_filters = Q()

    for filter_value in filters:
        if filter_value.startswith("!"):
            exclude_filters |= Q(**{f"{field_name}": filter_value[1:]})
        else:
            include_filters |= Q(**{f"{field_name}": filter_value})

    return queryset.filter(include_filters).exclude(exclude_filters)
class Query(graphene.ObjectType):
    animes = graphene.List(AnimeType,
                               limit=graphene.Int(), page=graphene.Int(),
                                order=OrderEnum(), kind=AnimeKindString(),
                                status=StatusString(), seasong=SeasonString(),
                                season=SeasonString(), score=graphene.Int(),
                                duration=DurationString(), rating=RatingString(),
                                genre=graphene.String(), studio=graphene.String(),
                                censored=graphene.Boolean(), id=graphene.String(),
                                excludedId=graphene.String(), search=graphene.String(),
                           )


    def resolve_animes(self, info,search=None,genre=None,studio=None,censored=None,franchise=None,id=None,excludedId=None,duration=None,kind=None,rating=None, status=None, season=None, score=0, limit=10, page=1, order=OrderEnum.ID, **kwargs):
        queryset = Anime.objects.all()
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        if studio is not None:
            queryset = queryset.filter(studio=studio)
        if franchise is not None:
            queryset = queryset.filter(franchise=franchise)
        if censored is not None:
            queryset = queryset.filter(censored=censored)
        if id is not None:
            ids = id.split(',')
            queryset = queryset.filter(id__in=ids)
        if excludedId is not None:
            excludedIds = excludedId.split(',')
            queryset = queryset.exclude(id__in=excludedIds)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        if kind:
            queryset = filter_by_field(queryset, 'kind', kind)
        if status:
            queryset = filter_by_field(queryset, 'status', status)
        if season:
            queryset = filter_by_field(queryset, 'season', season)
        if score:
            queryset = queryset.filter(score__gte=score)
        if rating:
            queryset = filter_by_field(queryset, 'rating', rating)
        if duration:
            if duration == 'S':
                queryset = queryset.filter(duration__lte=10)
            elif duration == '!S':
                queryset = queryset.filter(duration__gte=10)
            elif duration == 'D':
                queryset = queryset.filter(duration__lte=30)
            elif duration == '!D' or duration == 'F':
                queryset = queryset.filter(duration__gte=30)
            elif duration == '!F':
                queryset = queryset.filter(duration__lte=30)
        if order == OrderEnum.RANDOM:
            queryset = queryset.order_by("?")
        elif order == OrderEnum.RANKED_RANDOM:
            queryset = queryset.filter(score__isnull=False).order_by("?")
        elif order == OrderEnum.RANKED_SHIKI:
            queryset = queryset.order_by("-score")
        elif order == OrderEnum.ID_DESC:
            queryset = queryset.order_by("-id")
        elif order == OrderEnum.CREATED_AT_DESC:
            queryset = queryset.order_by("-createdAt")
        else:
            queryset = queryset.order_by(order.value)

        offset = limit * (page - 1)
        queryset = queryset[offset:offset + limit]

        return queryset

schema = graphene.Schema(query=Query)