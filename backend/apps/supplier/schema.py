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


# MUTATIONS


# CREATE
class CreateSupplierMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        website = graphene.String(required=True)
        login = graphene.String(required=True)
    # The class attributes define the response of the mutation
    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, root, info, name, website, login):
        supplier = Supplier.objects.create(
            name=name, website=website, login=login)

        # Notice we return an instance of this mutation
        return CreateSupplierMutation(supplier=supplier)


# UPDATE
class UpdateSupplierMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=False)
        website = graphene.String(required=False)
        login = graphene.String(required=False)
    # The class attributes define the response of the mutation
    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, root, info, id, name, website, login):
        supplier = Supplier.objects.get(pk=id)
        if name is not None:
            supplier.name = name
        if website is not None:
            supplier.website = website
        if login is not None:
            supplier.login = login
        supplier.save()

        # Notice we return an instance of this mutation
        return UpdateSupplierMutation(supplier=supplier)


# DELETE
class DeleteSupplierMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            supplier = Supplier.objects.get(pk=id)
            supplier.delete()
        except Supplier.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteSupplierMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_supplier = CreateSupplierMutation.Field()
    update_supplier = UpdateSupplierMutation.Field()
    delete_supplier = DeleteSupplierMutation.Field()
