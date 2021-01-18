from mutations.delete_mutation import DeleteMutation
from graphene import ObjectType
from ..graphene_django_type import (
    IsolatedModelType,
    RelationshipReceiverModelType,
    RelationshipSenderModelType,
)


class DeleteIsolatedType(DeleteMutation):
    class Meta:
        graphene_type = IsolatedModelType


class DeleteRelationshipReceiverType(DeleteMutation):
    class Meta:
        graphene_type = RelationshipReceiverModelType


class DeleteRelationshipSenderType(DeleteMutation):
    class Meta:
        graphene_type = RelationshipSenderModelType


class DeleteMutations(ObjectType):
    delete_isolated_type = DeleteIsolatedType.Field()
    delete_relationship_receiver_type = DeleteRelationshipReceiverType.Field()
    delete_relationship_sender_type = DeleteRelationshipSenderType.Field()
