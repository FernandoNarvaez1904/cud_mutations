import graphene
from .custom_mutation_base import CustomMutationBase
from .utils import enforce_custom_auth_decorator, get_graphene_arguments


class DeleteMutation(graphene.Mutation, CustomMutationBase):

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        interfaces=(),
        possible_types=(),
        default_resolver=None,
        _meta=None,
        **options
    ):
        cls.set_extra_arguments(cls, options)

        cls.set_custom_auth(cls, options)

        cls.set_extra_info(cls, options)

        cls.set_graphene_type(cls, options)

        graphene_arguments_generator = get_graphene_arguments(cls.graphene_type)
        for i in graphene_arguments_generator:
            pass

        return super().__init_subclass_with_meta__(
            interfaces=interfaces,
            possible_types=possible_types,
            default_resolver=default_resolver,
            _meta=_meta,
            **options
        )

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
