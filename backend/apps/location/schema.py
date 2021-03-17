import graphene
from graphene import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Building
from .models import Floor
from .models import Room


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building
        filter_fields = ['name']
        interfaces = (Node,)


class FloorType(DjangoObjectType):
    class Meta:
        model = Floor
        filter_fields = ['name', 'batiment']
        interfaces = (Node,)


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = ['name', 'floor']
        interfaces = (Node,)


class RoomBType(DjangoObjectType):
    class Meta:
        model = Room


class Query(graphene.ObjectType):
    buildings = graphene.List(BuildingType)
    floors = graphene.List(FloorType)
    rooms = graphene.List(RoomBType)

    filtRooms = DjangoFilterConnectionField(RoomType)
    room = Node.Field(RoomType)

    floors = DjangoFilterConnectionField(FloorType)
    floor = Node.Field(FloorType)

    buildings = DjangoFilterConnectionField(BuildingType)
    building = Node.Field(BuildingType)

    def resolve_buildings(self, info, **kwargs):
        return Building.objects.all()

    def resolve_floors(self, info, **kwargs):
        return Floor.objects.all()

    def resolve_rooms(self, info, **kwargs):
        return Room.objects.all()
