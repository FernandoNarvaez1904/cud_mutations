from mutations.create_mutation import CreateMutation
from graphene import ObjectType
from ..graphene_django_type import (
    IsolatedModelType,
    RelationshipReceiverModelType,
    RelationshipSenderModelType,
)


class CreateIsolatedType(CreateMutation):
    class Meta:
        graphene_type = IsolatedModelType
        is_required = ["number", "textField"]


class CreateRelationshipReceiverType(CreateMutation):
    class Meta:
        graphene_type = RelationshipReceiverModelType


class CreateRelationshipSenderType(CreateMutation):
    class Meta:
        graphene_type = RelationshipSenderModelType


class CreateMutations(ObjectType):
    create_isolated_type = CreateIsolatedType.Field()
    create_relationship_receiver_type = CreateRelationshipReceiverType.Field()
    create_relationship_sender_type = CreateRelationshipSenderType.Field()
