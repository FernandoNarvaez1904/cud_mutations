from six import indexbytes
from .mutation_base import MutationBase
import graphene


class UpdateMutation(MutationBase):

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

            id = query_fields.pop("id")

            # Cleaning query_fields
            query_fields.pop("extra_arguments")
            relationship_queries = cls.pop_formatted_relationship_queries(
                cls, query_fields)
            cls.pop_manual_resolve_arguments(
                cls, model, query_fields)

            # Getting relationships from fields
            query_fields = {**query_fields, **
                            relationship_queries["foreign_key"]}
            
            query_model = model.objects.get(pk=id)

            for field in query_fields:
                setattr(query_fields,field.__name__, field)
            
            for name, value in relationship_queries["many_to_many"]["add"].items():
                for id in value:
                    rel = getattr(query_model, name)
                    obj = rel.model.objects.get(pk=id)
                    rel.add(obj)
            
            for name, value in relationship_queries["many_to_many"]["rmv"].items():
                for id in value:
                    try:
                        getattr(query_model, name).remove(id)
                    except:
                        raise Exception(f"Cannot remove from {name} just replace from the other end")
        
            query_model.save()

        except Exception as e:
            return UpdateMutation(messages=[str(e)], completed=False)

        response = UpdateMutation(messages=["Added"], completed=True)
        setattr(response, cls.graphene_type.__name__, query_model)
        return response

    class Arguments:
        id = graphene.ID(required=True)