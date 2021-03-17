import graphene
from graphene_django import DjangoObjectType

from .models import Asset


class AssetType(DjangoObjectType):
    class Meta:
        model = Asset


class Query(graphene.ObjectType):
    Assets = graphene.List(AssetType)

    def resolve_Assets(self, info, **kwargs):
        return Asset.objects.all()