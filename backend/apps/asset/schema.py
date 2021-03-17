import graphene
from graphene_django import DjangoObjectType

from .models import Asset
from ..supplier.schema import SupplierType
from ..team.schema import TeamType


class AssetType(DjangoObjectType):
    class Meta:
        model = Asset


class Query(graphene.ObjectType):
    Assets = graphene.List(AssetType)

    def resolve_Assets(self, info, **kwargs):
        return Asset.objects.all()
        
# MUTATIONS


# CREATE
class CreateAssetMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        picture = graphene.String()
        cost = graphene.Float()
        supplier_id = graphene.ID()
        team_id = graphene.ID()

    # The class attributes define the response of the mutation
    asset = graphene.Field(AssetType)

    @classmethod
    def mutate(cls, root, info, name, description, picture, cost, supplier_id, team_id):
        asset = Asset.objects.create(name=name, description=description, picture=picture, cost=cost, supplier_id=supplier_id, team_id=team_id)

        # Notice we return an instance of this mutation
        return CreateAssetMutation(asset=asset)


# UPDATE
class UpdateAssetMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=True)
        description = graphene.String()
        picture = graphene.String()
        cost = graphene.Float()
        supplier_id = graphene.ID()
        team_id = graphene.ID()


    # The class attributes define the response of the mutation
    asset = graphene.Field(AssetType)

    @classmethod
    def mutate(cls, root, info, id, name, description, picture, cost, supplier_id, team_id):
        asset = Asset.objects.get(pk=id)
        asset.name = name
        if description is not None:
            asset.description = description
        if picture is not None:
            asset.picture = picture
        if cost is not None:
            asset.cost = cost
        asset.supplier_id = supplier_id
        asset.team_id = team_id
        asset.save()

        # Notice we return an instance of this mutation
        return UpdateAssetMutation(asset=asset)


# DELETE
class DeleteAssetMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            asset = Asset.objects.get(pk=id)
            asset.delete()
        except Asset.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteAssetMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_asset = CreateAssetMutation.Field()
    update_asset = UpdateAssetMutation.Field()
    delete_asset = DeleteAssetMutation.Field()