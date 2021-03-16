import graphene
from graphene_django import DjangoObjectType

from .models import Building
from .models import Floor
from .models import Room


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building


class FloorType(DjangoObjectType):
    class Meta:
        model = Floor


class RoomType(DjangoObjectType):
    class Meta:
        model = Room


class Query(graphene.ObjectType):
    buildings = graphene.List(BuildingType)
    floors = graphene.List(FloorType)
    rooms = graphene.List(RoomType)

    def resolve_buildings(self, info, **kwargs):
        return Building.objects.all()

    def resolve_floors(self, info, **kwargs):
        return Floor.objects.all()

    def resolve_rooms(self, info, **kwargs):
        return Room.objects.all()
