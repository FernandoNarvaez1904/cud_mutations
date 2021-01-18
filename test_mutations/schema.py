import graphene
from .mutations.mutations import Mutations
from .graphene_django_type import IsolatedModelType
from .query import Query


schema = graphene.Schema(
    query=Query,
    mutation=Mutations,
    auto_camelcase=True,
)
