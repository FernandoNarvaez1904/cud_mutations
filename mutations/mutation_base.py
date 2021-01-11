from mutations.mutation_argument import MutationArgument
from typing import Generator
import graphene
from .validator import Validator


class MutationBase(graphene.Mutation):

    # Default field to return from the mutation
    completed = graphene.Boolean()
    messages = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        pass

    def format_extra_arguments(extra_arguments: list,  is_required: list = []) -> Generator:
        if Validator.validate_extra_arguments(extra_arguments):
            for argument in extra_arguments:

                argument_names = argument[0]
                scalar = argument[1]

                display_name = ""
                property_name = ""
                # If argument_name has property_name
                if isinstance(argument_names, tuple):
                    display_name = argument_names[0]
                    property_name = argument_names[1]
                # Else property_name will be the same as display_name
                else:
                    display_name = argument_names
                    property_name = argument_names

                is_property = True
                if len(argument) > 2:
                    is_property = argument[2]

                # If name is required
                arg_is_required = display_name in is_required

                yield MutationArgument(
                    display_name=display_name,
                    property_name=property_name,
                    is_property=is_property,
                    is_required=arg_is_required,
                    graphene_scalar=scalar
                )

    def format_graphene_arguments(graphene_type, is_required=[]):
        # Accessing specific place in graph type that has all options needed
        graphene_type_options = graphene_type._meta.class_type._meta.__dict__
        # Getting all the fields in the type
        fields = graphene_type_options.get("fields")

        for name, field in fields.items():
            # Field comes from the type directly, so it's assumed that is a property
            is_property = True
            arg_is_required = name in is_required

            is_relationship = False
            scalar = None
            if field_type := field.__dict__.get("_type"):
                # If it is not a graphene scalar, but a graphene structure like,
                # nonNull, the actual scalar will be inside of the "of_type"
                # key in the structure object.__dict__
                # If field it's not an structure, then
                # the field is the scalar
                gp_of_type = field_type.__dict__.get("_of_type")

                scalar = gp_of_type(required=arg_is_required) if gp_of_type else field_type(
                    required=arg_is_required)

            # If the field is a relationship
            elif callable(field.type):
                is_relationship = True
                scalar = graphene.String(required=True)

            yield MutationArgument(
                display_name=name,
                property_name=name,
                graphene_scalar=scalar,
                is_required=arg_is_required,
                is_property=is_property,
                is_relationship=is_relationship,
            )

    def set_arguments(self, options):
        # Getting and Setting Extra Arguments
        extra_arguments = self.format_extra_arguments(
            options.get("extra_arguments"))

        self.set_graphene_type(self, options)
        graphene_type_argument = self.format_graphene_arguments(
            self.graphene_type)

        if not hasattr(self, "Arguments"):
            setattr(self, "Arguments", type("Arguments", (), {}))
            
        arguments_info = {}
        for argument in extra_arguments:
            setattr(self.Arguments, argument.display_name, argument.of_type)
            arguments_info[argument.display_name] = argument

        for argument in graphene_type_argument:
            setattr(self.Arguments, argument.display_name, argument.of_type)
            arguments_info[argument.display_name] = argument

        setattr(self, "arguments_info", arguments_info)

    def get_model(self):
        return self.graphene_type._meta.model

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
        valid_extra_info = Validator.validate_extra_info(extra_info)
        self.extra_info = {}

        if valid_extra_info:
            for info in extra_info:
                self.extra_info[info[0]] = info[1]

    def set_graphene_type(self, options):
        graphene_type = options.get("graphene_type")

        if Validator.validate_graphene_type(graphene_type):
            self.graphene_type = graphene_type
