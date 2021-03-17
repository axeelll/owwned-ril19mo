import graphene
from graphene_django import DjangoObjectType

from .models import Supplier


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier


class Query(graphene.ObjectType):
    suppliers = graphene.List(SupplierType)

    def resolve_suppliers(self, info, **kwargs):
        return Supplier.objects.all()
