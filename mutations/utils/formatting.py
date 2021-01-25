import graphene
from typing import Any, Generator

from graphene.types.scalars import Scalar
from ..validator import Validator
from ..mutation_argument import MutationArgument

def format_extra_arguments(extra_arguments: list,  is_required: list = []) -> Generator:
    if Validator.validate_extra_arguments(extra_arguments):
        for argument in extra_arguments:
            argument_names = argument[0]

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

            scalar = argument[1]

            # If name is required
            arg_is_required = display_name in is_required
            if arg_is_required:
                if isinstance(argument[1],Scalar):
                    scalar = graphene.NonNull(argument[1].__class__)
                else:
                    scalar = graphene.NonNull(argument[1])


            yield MutationArgument(
                display_name=display_name,
                property_name=property_name,
                is_property=is_property,
                is_required=arg_is_required,
                graphene_scalar=scalar
            )

def format_graphene_arguments(graphene_type: Any, is_required: list =[]) -> Generator:
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
