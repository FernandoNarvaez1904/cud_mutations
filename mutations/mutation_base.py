import graphene
from .validator import Validator
from .utils.formatting import format_extra_arguments, format_graphene_arguments
from .utils.security import enforce_custom_auth_decorator


class MutationBase(graphene.Mutation):

    # Default field to return from the mutation
    completed = graphene.Boolean()
    messages = graphene.List(graphene.String)

    @classmethod
    @enforce_custom_auth_decorator
    def mutate(cls, root, info, **kwargs):

        # Extract extra arguments and converting to one element
        extra_arguments = {}
        for i in cls.extra_argument_names:
            if i in kwargs:
                extra_arguments[i] = kwargs.pop(i)
        kwargs["extra_arguments"] = extra_arguments

        cls.before_mutate(cls, root, info, **kwargs)
        rt = cls.mutate_method(cls, root, info, **kwargs)
        cls.after_mutate(cls, root, info, **kwargs)

        return rt

    def get_model(self):
        return self.graphene_type._meta.model

    def set_graphene_arguments(self, options):

        is_required = []
        if required := options.get("is_required"):
            is_required = required

        self.set_graphene_type(self, options)
        graphene_type_argument = format_graphene_arguments(
            self.graphene_type, is_required)

        if not hasattr(self, "Arguments"):
            setattr(self, "Arguments", type("Arguments", (), {}))

        for argument in graphene_type_argument:
            setattr(self.Arguments, argument.display_name, argument.of_type)


    def set_extra_arguments(self, options):

        is_required = []
        if required := options.get("is_required"):
            is_required = required

        # Getting and Setting Extra Arguments
        extra_arguments = format_extra_arguments(
            options.get("extra_arguments"), is_required)

        if not hasattr(self, "Arguments"):
            setattr(self, "Arguments", type("Arguments", (), {}))

        setattr(self, "extra_argument_names", [])
        for argument in extra_arguments:
            setattr(self.Arguments, argument.display_name, argument.of_type)
            self.extra_argument_names.append(argument.display_name)

    def set_custom_auth(self, options):
        custom_auth = options.get("custom_auth")
        # If auth validation fails, creating a default_auth
        if not Validator.validate_custom_auth(custom_auth):

            def default_auth(*args, **kwargs):
                return (True, [])

            setattr(self, "custom_auth", default_auth)
        else:
            setattr(self, "custom_auth", custom_auth)

    def set_extra_info(self, options):
        extra_info = options.get("extra_info")
        if Validator.validate_extra_info(extra_info):
            self.extra_info = extra_info

    def set_graphene_type(self, options):
        graphene_type = options.get("graphene_type")
        if Validator.validate_graphene_type(graphene_type):
            self.graphene_type = graphene_type

    def set_before_mutate(self, options):
        before_mutate = options.get("before_mutate")
        if not Validator.validate_mutation_functions(before_mutate):
            def default_mutate(*args, **kwargs):
                pass
            before_mutate = default_mutate
        self.before_mutate = before_mutate

    def set_mutate_method(self, mutate_method):
        if not Validator.validate_mutation_functions(mutate_method):
            raise Exception(
                "Mutation instance needs a mutation_method property")
        self.mutate_method = mutate_method

    def set_after_mutate(self, options):
        after_mutate = options.get("after_mutate")
        if not Validator.validate_mutation_functions(after_mutate):
            def default_mutate(*args, **kwargs):
                pass
            after_mutate = default_mutate
        self.after_mutate = after_mutate
