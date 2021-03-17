import graphene

from apps.organization import schema as organization_schema
from apps.supplier import schema as supplier_schema
from apps.team import schema as team_schema
from apps.asset import schema as asset_schema
from apps.history_event import schema as history_event_schema


class Query(history_event_schema.Query, asset_schema.Query, team_schema.Query, supplier_schema.Query, organization_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
