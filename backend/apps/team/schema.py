import graphene
from graphene_django import DjangoObjectType

from .models import Team


class TeamType(DjangoObjectType):
    class Meta:
        model = Team


class Query(graphene.ObjectType):
    teams = graphene.List(TeamType)

    def resolve_teams(self, info, **kwargs):
        return Team.objects.all()