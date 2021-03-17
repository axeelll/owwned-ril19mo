import graphene
from graphene_django import DjangoObjectType

from .models import Team
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class TeamType(DjangoObjectType):
    class Meta:
        model = Team


class Query(graphene.ObjectType):
    teams = graphene.List(TeamType)

    def resolve_teams(self, info, **kwargs):
        return Team.objects.all()
        
# MUTATIONS


# CREATE
class CreateTeamMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        manager_id = graphene.ID()

    # The class attributes define the response of the mutation
    team = graphene.Field(TeamType)

    @classmethod
    def mutate(cls, root, info, name, manager_id):
        team = Team.objects.create(name=name, manager_id=manager_id)

        # Notice we return an instance of this mutation
        return CreateTeamMutation(team=team)


# UPDATE
class UpdateTeamMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=True)
        manager = graphene.ID()

    # The class attributes define the response of the mutation
    team = graphene.Field(TeamType)

    @classmethod
    def mutate(cls, root, info, id, name, manager = None):
        team = Team.objects.get(pk=id)
        team.name = name
        if not manager: 
            team.manager = manager
        team.save()

        # Notice we return an instance of this mutation
        return UpdateTeamMutation(team=team)


# DELETE
class DeleteTeamMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            team = Team.objects.get(pk=id)
            team.delete()
        except Team.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteTeamMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_team = CreateTeamMutation.Field()
    update_team = UpdateTeamMutation.Field()
    delete_team = DeleteTeamMutation.Field()