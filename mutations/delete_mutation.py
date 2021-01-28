import graphene
from .mutation_base import MutationBase

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
        cls.set_graphene_type(cls, options, False)

        cls.set_extra_arguments(cls, options)

        cls.set_custom_auth(cls, options)

        cls.set_extra_info(cls, options)

        cls.set_before_mutate(cls, options)

        cls.set_after_mutate(cls, options)

        cls.set_mutate_method(cls, cls.mutate_method)

        return super().__init_subclass_with_meta__(
            interfaces=interfaces,
            possible_types=possible_types,
            default_resolver=default_resolver,
            _meta=_meta,
            **options
        )

    def mutate_method(cls, root, info, *args, **kwargs):
        ids = kwargs.get("id")
        model = cls.get_model(cls)

        queries = []
        for id in ids:
            try:
                # Quering and deleting
                queries.append(model.objects.get(id=id))
            except Exception:
                # If quering failed returning error
                errors = [f"{model.__name__} with id '{id}' doesn't exist."]
                return DeleteMutation(messages=errors, completed=False, )

        for query in queries:
            query.delete()
        # Returning successfully
        return DeleteMutation(completed=True)

    class Arguments:
        id = graphene.List(graphene.ID, required=True)


