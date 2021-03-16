import graphene

from apps.organization import schema as organization_schema
from apps.supplier import schema as supplier_schema
from apps.team import schema as team_schema
from apps.asset import schema as asset_schema


class Query(asset_schema.Query, team_schema.Query, supplier_schema.Query, organization_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
