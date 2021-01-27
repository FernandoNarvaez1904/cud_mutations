import graphene
from .graphene_django_type import IsolatedModelType, RelationshipReceiverModelType
from .models import IsolatedModel, RelationshipReceiverModel


class IsolatedModelQuery(graphene.ObjectType):

    all_isolated_models = graphene.List(IsolatedModelType)

    def resolve_all_isolated_models(self, info):
        return IsolatedModel.objects.all()

class RelationshipReceiverQuery(graphene.ObjectType):

    all_relationship_receiver = graphene.List(RelationshipReceiverModelType)

    def resolve_all_relationship_receiver(self, info):
        return RelationshipReceiverModel.objects.all()


class Query(
    IsolatedModelQuery,
    RelationshipReceiverQuery,
):
    pass
