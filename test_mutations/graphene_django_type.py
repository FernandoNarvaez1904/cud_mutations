import graphene
from graphene_django import DjangoObjectType
from .models import IsolatedModel, RelationshipReceiverModel, RelationshipSenderModel


class IsolatedModelType(DjangoObjectType):
    number = graphene.Int()

    class Meta:
        model = IsolatedModel

    def resolve_number(self, info):
        return 25


class RelationshipReceiverModelType(DjangoObjectType):
    class Meta:
        model = RelationshipReceiverModel


class RelationshipSenderModelType(DjangoObjectType):
    class Meta:
        model = RelationshipSenderModel
