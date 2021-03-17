import graphene
from graphene_django import DjangoObjectType

from .models import HistoryEvent


class HistoryEventType(DjangoObjectType):
    class Meta:
        model = HistoryEvent


class Query(graphene.ObjectType):
    history_events = graphene.List(HistoryEventType)

    def resolve_history_events(self, info, **kwargs):
        return HistoryEvent.objects.all()
