from mutations.update_mutation import UpdateMutation
from graphene import ObjectType
from ..graphene_django_type import (
    IsolatedModelType,
    RelationshipReceiverModelType,
    RelationshipSenderModelType,
)

class UpdateIsolatedType(UpdateMutation):
    class Meta:
        graphene_type = IsolatedModelType


class UpdateRelationshipReceiverType(UpdateMutation):
    class Meta:
        graphene_type = RelationshipReceiverModelType


class UpdateRelationshipSenderType(UpdateMutation):
    class Meta:
        graphene_type = RelationshipSenderModelType


class UpdateMutations(ObjectType):
    update_isolated_type = UpdateIsolatedType.Field()
    update_relationship_receiver_type = UpdateRelationshipReceiverType.Field()
    update_relationship_sender_type = UpdateRelationshipSenderType.Field()
