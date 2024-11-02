import graphene
from graphene_django.types import DjangoObjectType
from .models import Anime

class AnimeType(DjangoObjectType):
    class Meta:
        model = Anime