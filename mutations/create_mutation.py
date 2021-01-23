from .mutation_base import MutationBase

class CreateMutation(MutationBase):

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

        cls.set_graphene_arguments(cls, options)

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
        return CreateMutation(messages= ["Added"], completed=True) 

