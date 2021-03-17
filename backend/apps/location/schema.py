import graphene
from graphene import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

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


# MUTATIONS BUILDING
# CREATE
class CreateBuildingMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        lat = graphene.Float(required=True)
        lng = graphene.Float(required=True)
        address = graphene.String(required=True)
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    building = graphene.Field(BuildingType)

    @classmethod
    def mutate(cls, root, info, lat, lng, address, name):
        building = Building.objects.create(
            lat=lat, lng=lng, address=address, name=name)

        # Notice we return an instance of this mutation
        return CreateBuildingMutation(building=building)


# UPDATE
class UpdateBuildingMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        lat = graphene.Float(required=False)
        lng = graphene.Float(required=False)
        address = graphene.String(required=False)
        name = graphene.String(required=False)

    # The class attributes define the response of the mutation
    building = graphene.Field(BuildingType)

    @classmethod
    def mutate(cls, root, info, id, lat=None, lng=None, address=None, name=None):
        node_type, pk = from_global_id(id)
        building = Building.objects.get(pk=pk)
        if lat is not None:
            building.lat = lat
        if lng is not None:
            building.lng = lng
        if address is not None:
            building.address = address
        if name is not None:
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
            node_type, pk = from_global_id(id)
            building = Building.objects.get(pk=pk)
            building.delete()
        except Building.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteBuildingMutation(deleted=deleted)


# MUTATIONS FLOOR
# CREATE
class CreateFloorMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        number = graphene.Int(required=True)
        batiment_id = graphene.GlobalID(required=False, name="batiment")

    # The class attributes define the response of the mutation
    floor = graphene.Field(FloorType)

    @classmethod
    def mutate(cls, root, info, name, number, batiment_id):
        node_type, batiment_pk = from_global_id(batiment_id)
        floor = Floor.objects.create(
            name=name, number=number, batiment_id=batiment_pk)

        # Notice we return an instance of this mutation
        return CreateFloorMutation(floor=floor)


# UPDATE
class UpdateFloorMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=False)
        number = graphene.Int(required=False)
        batiment = graphene.GlobalID(required=False, name="floor")

    # The class attributes define the response of the mutation
    floor = graphene.Field(FloorType)

    @classmethod
    def mutate(cls, root, info, id, name=None, number=None, batiment_id=None):
        batiment_pk = None
        if batiment_id is not None:
            node_type, batiment_pk = from_global_id(batiment_id)
        floor = Floor.objects.get(pk=id)
        if name is not None:
            floor.name = name
        if number is not None:
            floor.number = number
        if batiment_pk is not None:
            floor.batiment_id = batiment_pk

        floor.save()

        # Notice we return an instance of this mutation
        return UpdateFloorMutation(floor=floor)


# DELETE
class DeleteFloorMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            floor = Floor.objects.get(pk=id)
            floor.delete()
        except Floor.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteFloorMutation(deleted=deleted)


# MUTATIONS ROOM
# CREATE
class CreateRoomMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        floor_id = graphene.GlobalID(name="floor")

    # The class attributes define the response of the mutation
    room = graphene.Field(RoomType)

    @classmethod
    def mutate(cls, root, info, name, floor_id):
        node_type, floor_pk = from_global_id(floor_id)
        room = Floor.objects.create(name=name, floor_id=floor_pk)

        # Notice we return an instance of this mutation
        return CreateFloorMutation(room=room)


# UPDATE
class UpdateRoomMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=True)
        floor_id = graphene.Int(name="floor")

    # The class attributes define the response of the mutation
    room = graphene.Field(RoomType)

    @classmethod
    def mutate(cls, root, info, id, name=None, floor_id=None):
        floor_pk = None
        if floor_id is not None:
            node_type, floor_pk = from_global_id(floor_id)
        room = Room.objects.get(pk=id)
        if name is not None:
            room.name = name
        if floor_id is not None:
            room.floor_id = floor_pk

        room.save()

        # Notice we return an instance of this mutation
        return UpdateRoomMutation(room=room)


# DELETE
class DeleteRoomMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            room = Room.objects.get(pk=id)
            room.delete()
        except Floor.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteRoomMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_floor = CreateFloorMutation.Field()
    update_floor = UpdateFloorMutation.Field()
    delete_floor = DeleteFloorMutation.Field()
    create_building = CreateBuildingMutation.Field()
    update_building = UpdateBuildingMutation.Field()
    delete_building = DeleteBuildingMutation.Field()
    create_room = CreateRoomMutation.Field()
    update_room = UpdateRoomMutation.Field()
    delete_room = DeleteRoomMutation.Field()
