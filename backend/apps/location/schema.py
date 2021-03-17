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
    rooms = DjangoFilterConnectionField(RoomType)
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

# MUTATIONS


# CREATE
class CreateBuildingMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        lat = graphene.Decimal(required=True)
        lng = graphene.Decimal(required=True)
        address = graphene.String(required=True)
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    building = graphene.Field(BuildingType)

    @classmethod
    def mutate(cls, root, info, lat, lng, address, name):
        building = Building.objects.create(lat=lat)
        building = Building.objects.create(lng=lng)
        building = Building.objects.create(address=address)
        building = Building.objects.create(name=name)

        # Notice we return an instance of this mutation
        return CreateBuildingMutation(building=building)


# UPDATE
class UpdateBuildingMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        lat = graphene.Decimal(required=True)
        lng = graphene.Decimal(required=True)
        address = graphene.String(required=True)
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    building = graphene.Field(BuildingType)

    @classmethod
    def mutate(cls, root, info, id, lat, lng, address, name):
        building = Organization.objects.get(pk=id)
        building.lat = lat
        building.lng = lng
        building.address = address
        building.name = name
        building.save()

        # Notice we return an instance of this mutation
        return UpdateBuildingMutation(building=building)


# DELETE
class DeleteBuildingMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            building = Building.objects.get(pk=id)
            building.delete()
        except Building.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteBuildingMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_building = CreateBuildingMutation.Field()
    update_building = UpdateBuildingMutation.Field()
    delete_building = DeleteBuildingMutation.Field()
