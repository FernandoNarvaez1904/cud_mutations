import graphene
from .graphene_django_type import IsolatedModelType
from .models import IsolatedModel


class IsolatedModelQuery(graphene.ObjectType):

    all_isolated_models = graphene.List(IsolatedModelType)

    def resolve_all_isolated_models():
        return IsolatedModel.objects.query.all()


class Query(
    IsolatedModelQuery,
):
    pass
