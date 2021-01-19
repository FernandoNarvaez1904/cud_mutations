import graphene
from .validator import Validator
from .utils.formatting import format_extra_arguments, format_graphene_arguments


class MutationBase(graphene.Mutation):

    # Default field to return from the mutation
    completed = graphene.Boolean()
    messages = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        cls.before_mutate(cls, root, info, **kwargs)
        rt = cls.mutate_method(cls, root, info, **kwargs)
        cls.after_mutate(cls, root, info, **kwargs)

        return rt

    def get_model(self):
        return self.graphene_type._meta.model
    
    def set_graphene_arguments(self, options):

        self.set_graphene_type(options)
        graphene_type_argument = format_graphene_arguments(
            self.graphene_type)

        if not hasattr(self, "Arguments"):
            setattr(self, "Arguments", type("Arguments", (), {}))

        arguments_info = {}
        for argument in graphene_type_argument:
            setattr(self.Arguments, argument.display_name, argument.of_type)
            arguments_info[argument.display_name] = argument

        if not hasattr(self, "arguments_info"):
            setattr(self, "arguments_info", arguments_info)
        else:
            current_arguments_info = options.get("arguments_info")
            self.arguments_info = {**current_arguments_info, **arguments_info}

    def set_extra_arguments(self, options):
        # Getting and Setting Extra Arguments
        extra_arguments = format_extra_arguments(
            options.get("extra_arguments"))

        if not hasattr(self, "Arguments"):
            setattr(self, "Arguments", type("Arguments", (), {}))

        arguments_info = {}
        for argument in extra_arguments:
            setattr(self.Arguments, argument.display_name, argument.of_type)
            arguments_info[argument.display_name] = argument

        if not hasattr(self, "arguments_info"):
            setattr(self, "arguments_info", arguments_info)
        else:
            current_arguments_info = options.get("arguments_info")
            self.arguments_info = {**current_arguments_info, **arguments_info}

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
            raise Exception("Mutation instance needs a mutation_method property")
        self.mutate_method = mutate_method
    
    def set_after_mutate(self, options):
        after_mutate = options.get("after_mutate")
        if not Validator.validate_mutation_functions(after_mutate):
            def default_mutate(*args, **kwargs):
                pass
            after_mutate = default_mutate
        self.after_mutate = after_mutate    
    