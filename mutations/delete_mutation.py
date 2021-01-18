import graphene
from .mutation_base import MutationBase
from .utils.security import enforce_custom_auth_decorator


class DeleteMutation(MutationBase):

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        interfaces=(),
        possible_types=(),
        default_resolver=None,
        _meta=None,
        **options
    ):
        cls.set_graphene_type(cls, options)

        cls.set_extra_arguments(options)

        cls.set_custom_auth(cls, options)

        cls.set_extra_info(cls, options)

        return super().__init_subclass_with_meta__(
            interfaces=interfaces,
            possible_types=possible_types,
            default_resolver=default_resolver,
            _meta=_meta,
            **options
        )
    class Arguments:
        id = graphene.ID(required=True)
    
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
            return DeleteMutation(messages=errors, completed=False, )
        # Returning successfully
        return DeleteMutation(completed=True)
