import graphene

from apps.organization import schema as organization_schema
from apps.supplier import schema as supplier_schema


class Query(supplier_schema.Query, organization_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
