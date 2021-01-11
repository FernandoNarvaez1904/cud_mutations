import graphene
from .mutation_base import MutationBase
from .utils import enforce_custom_auth_decorator, get_graphene_arguments


class DeleteMutation(MutationBase):

    class Arguments:
        id = graphene.String(required=True)

    @classmethod
    @enforce_custom_auth_decorator
    def mutate(cls, root, info, **kwargs):
        id = kwargs.get("id")
        model = cls.graphene_type._meta.model

        try:
            # Quering and deleting
            query = model.objects.get(id=id)
            query.delete()
        except Exception:
            # If quering failed returning error
            errors = [f"{model.__name__} with id '{id}' doesn't exist."]
            return DeleteMutation(errors=errors, completed=False, )
        # Returning successfully
        return DeleteMutation(completed=True)
