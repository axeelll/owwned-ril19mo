import graphene

from apps.organization import schema as organization_schema
from apps.team import schema as team_schema
from apps.asset import schema as asset_schema


class Query(organization_schema.Query, graphene.ObjectType):
    pass

class Query(team_schema.Query, graphene.ObjectType):
    pass

class Query(asset_schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)