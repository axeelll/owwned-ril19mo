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


# MUTATIONS BUILDING
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
        building = Building.objects.create(lat=lat, lng=lng, address=address, name=name)

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
        building = Building.objects.get(pk=id)
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


# MUTATIONS FLOOR
# CREATE
class CreateFloorMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        number = graphene.Int(required=True)
        batiment_id = graphene.Int(name="batiment")

    # The class attributes define the response of the mutation
    floor = graphene.Field(FloorType)

    @classmethod
    def mutate(cls, root, info, name, number, batiment_id):
        floor = Floor.objects.create(name=name, number=number, batiment_id=batiment_id)

        # Notice we return an instance of this mutation
        return CreateFloorMutation(floor=floor)


# UPDATE
class UpdateFloorMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=True)
        batiment = graphene.Int(name="floor")

    # The class attributes define the response of the mutation
    floor = graphene.Field(FloorType)

    @classmethod
    def mutate(cls, root, info, id, name, number, batiment_id):
        floor = Floor.objects.get(pk=id)
        floor.name = name
        floor.number = number
        floor.batiment_id = batiment_id

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
        floor_id = graphene.Int(name="floor")

    # The class attributes define the response of the mutation
    room = graphene.Field(RoomType)

    @classmethod
    def mutate(cls, root, info, name, floor_id):
        room = Floor.objects.create(name=name, floor_id=floor_id)

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
    def mutate(cls, root, info, id, name, number, floor_id):
        room = Room.objects.get(pk=id)
        room.name = name
        room.floor_id = floor_id

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
