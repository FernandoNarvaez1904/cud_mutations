from inspect import Arguments
import graphene
from graphene.types import argument
from .utils import (
    validate_extra_arguments,
    validate_custom_auth,
    validate_extra_info,
    validate_graphene_type,
    get_graphene_arguments,
)


class CustomMutationBase():
    # Return of the mutation
    completed = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def set_extra_arguments(self, options):
        # Getting and Setting Extra Arguments
        extra_arguments = validate_extra_arguments(
            options.get("extra_arguments"))
        extra_arguments_info = {}
        for argument in extra_arguments:

            setattr(self.Arguments, argument.display_name,
                    argument.of_type(required=argument.is_required))
            extra_arguments_info[argument.display_name] = argument

        setattr(self, "extra_arguments_info", extra_arguments_info)

    def set_custom_auth(self, options):
        custom_auth = options.get("custom_auth")
        # If auth validation fails, creating a default_auth
        if not validate_custom_auth(custom_auth):

            def default_auth(*args, **kwargs):
                return (True, [])

            setattr(self, "custom_auth", default_auth)
        else:
            setattr(self, "custom_auth", custom_auth)

    def set_extra_info(self, options):
        extra_info = validate_extra_info(options.get("extra_info"))
        self.extra_info = {}

        for info in extra_info:
            self.extra_info[info[0]] = info[1]

    def set_graphene_type(self, options):
        graphene_type = options.get("graphene_type")

        if validate_graphene_type(graphene_type):
            self.graphene_type = graphene_type
    
    def set_graphene_argument(self, options):
        pass