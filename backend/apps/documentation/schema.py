import graphene
from graphene_django import DjangoObjectType

from .models import Documentation


class DocumentationType(DjangoObjectType):
    class Meta:
        model = Documentation


class Query(graphene.ObjectType):
    documentations = graphene.List(DocumentationType)

    def resolve_documentations(self, info, **kwargs):
        return Documentation.objects.all()


# MUTATIONS


# CREATE
class CreateDocumentationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        url = graphene.String(required=False)
        doc_file = graphene.String(required=False)
        asset_id = graphene.ID()
    # The class attributes define the response of the mutation
    documentation = graphene.Field(DocumentationType)

    @classmethod
    def mutate(cls, root, info, asset_id, name=None, description=None, url=None, doc_file=None):
        documentation = Documentation.objects.create(
            name=name, description=description, url=url, doc_file=doc_file, asset_id=asset_id)

        # Notice we return an instance of this mutation
        return CreateDocumentationMutation(documentation=documentation)


# UPDATE
class UpdateDocumentationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        url = graphene.String(required=False)
        doc_file = graphene.String(required=False)

    # The class attributes define the response of the mutation
    documentation = graphene.Field(DocumentationType)

    @classmethod
    def mutate(cls, root, info, id, name=None, description=None, url=None, doc_file=None):
        documentation = Documentation.objects.get(pk=id)
        if name is not None:
            documentation.name = name
        if description is not None:
            documentation.description = description
        if url is not None:
            documentation.url = url
        if doc_file is not None:
            documentation.doc_file = doc_file
        documentation.save()

        # Notice we return an instance of this mutation
        return UpdateDocumentationMutation(documentation=documentation)


# DELETE
class DeleteDocumentationMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    deleted = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        deleted = True
        try:
            documentation = Documentation.objects.get(pk=id)
            documentation.delete()
        except Documentation.DoesNotExist:
            deleted = False

        # Notice we return an instance of this mutation
        return DeleteDocumentationMutation(deleted=deleted)


# MUTATIONS
class Mutation(graphene.ObjectType):
    create_documentation = CreateDocumentationMutation.Field()
    update_documentation = UpdateDocumentationMutation.Field()
    delete_documentation = DeleteDocumentationMutation.Field()
