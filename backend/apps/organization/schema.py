import graphene
from graphene_django import DjangoObjectType

from .models import Organization


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization


class Query(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)

    def resolve_organizations(self, info, **kwargs):
        return Organization.objects.all()


# MUTATIONS


# CREATE
class CreateOrganizationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    organization = graphene.Field(OrganizationType)

    @classmethod
    def mutate(cls, root, info, name):
        organization = Organization.objects.create(name=name)

        # Notice we return an instance of this mutation
        return CreateOrganizationMutation(organization=organization)


# UPDATE
class UpdateOrganizationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    organization = graphene.Field(OrganizationType)

    @classmethod
    def mutate(cls, root, info, id, name):
        organization = Organization.objects.get(pk=id)
        organization.name = name
        organization.save()

        # Notice we return an instance of this mutation
        return UpdateOrganizationMutation(organization=organization)


# DELETE
class DeleteOrganizationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            organization = Organization.objects.get(pk=id)
            organization.delete()
        except Organization.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteOrganizationMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_organization = CreateOrganizationMutation.Field()
    update_organization = UpdateOrganizationMutation.Field()
    delete_organization = DeleteOrganizationMutation.Field()