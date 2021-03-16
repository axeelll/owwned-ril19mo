import graphene

from apps.organization import schema as organization_schema


class Query(organization_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)