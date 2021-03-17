import graphene

from apps.organization import schema as organization_schema
from apps.location import schema as location_schema


class Query(organization_schema.Query, location_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
