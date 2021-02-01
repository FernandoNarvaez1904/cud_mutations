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

        cls.set_graphene_arguments(cls, options, True)

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

        model = cls.get_model(cls)
        query_fields = {}
        try:
            # Deleting all arguments that are not field of the model
            query_fields = {**kwargs}

            # Cleaning query_fields
            query_fields.pop("extra_arguments")
            cls.pop_manual_resolve_arguments(
                cls, model, query_fields)

            # Getting relationships from fields
            relationship_queries = cls.pop_formatted_relationship_queries(
                cls, query_fields)
            query_fields = {**query_fields, **
                            relationship_queries["foreign_key"]}

            # Creating Model
            new_model = model(**query_fields)

            # Saving Query
            new_model.save()

            # Adding many_to_many
            for name, value in relationship_queries["many_to_many"]["add"].items():
                for id in value:
                    getattr(new_model, name).add(id)

        except Exception as e:
            return CreateMutation(messages=[str(e)], completed=False)

        response = CreateMutation(messages=["Added"], completed=True)
        setattr(response, cls.graphene_type.__name__, new_model)
        return response
