import graphene
from graphene_django import DjangoObjectType
from graphene_django.utils import is_valid_django_model
from .extra_argument import ExtraArgument


def enforce_custom_auth_decorator(function):
    def wrapper(*args, **kwargs):
        # Getting the necessary variables
        cls = args[0]
        info = args[2]

        # Validating auth
        auth = cls.custom_auth(cls=cls, user=info.context.user, **kwargs)

        # If auth failed, returning mutation with errors
        if not auth[0]:
            return cls(completed=False, errors=auth[1])

        # If auth succeeded continuing with the execution
        rt = function(*args, **kwargs)
        return rt
    return wrapper


def validate_extra_arguments(extra_arguments, is_required=[]):
    if extra_arguments:
        if not isinstance(extra_arguments, list):
            raise Exception("extra_arguments needs to be a list")

        for argument in extra_arguments:
            if not isinstance(argument, tuple):
                raise Exception(
                    "extra_arguments needs to be a tuple: (names, graphene_type, is_property)")
            if not issubclass(argument[1], graphene.Scalar):
                raise Exception(
                    "extra_arguments second value in tuple needs to be a scalar")

            argument_instance = ExtraArgument()
            argument_name = argument[0]
            argument_type = argument[1]

            # If argument_name has property_name
            if isinstance(argument_name, tuple):
                argument_instance.display_name = argument_name[0]
                argument_instance.property_name = argument_name[1]
            # Else property_name will be the same as display_name
            else:
                argument_instance.display_name = argument_name
                argument_instance.property_name = argument_name

            # If argument has is_property
            if len(argument) >= 3:
                if not isinstance(argument[2], bool):
                    raise Exception(
                        "extras arguments third value in tuple needs to be a bool")
                argument_instance.is_property = argument[2]
            # If not is defaulted to True
            else:
                argument_instance.is_property = True

            # If name is required
            if argument_instance.display_name in is_required:
                argument_instance.is_required = True

            argument_instance.of_type = argument_type

            yield argument_instance

    return []


def validate_custom_auth(custom_auth):
    if custom_auth:
        if not callable(custom_auth):
            raise Exception("custom_auth needs to be a function")

        try:
            custom_auth_return = custom_auth()
        except:
            raise Exception(
                "Something failed in the validation of custom auth: \n" +
                " 1.Remember to Try-Except any logic that requires the usage of arguments.\n" +
                " 2.Returning or raising exceptions is not allowed, all failures in custom_auth" +
                " must be expressed as a value in the errors list\n" +
                " 3. The only return type accepted is a tuple like: (Boolean, messages)"
            )

        if not isinstance(custom_auth_return, tuple):
            raise Exception(
                "custom auth need to be a tuple like: (Boolean, messages)")

        if not isinstance(custom_auth_return[0], bool):
            raise Exception(
                "custom_auth first value in tuple, needs to be a boolean which represents the success of the auth")

        if not isinstance(custom_auth_return[1], list):
            raise Exception(
                "custom_auth second value in tuple, needs to be an instance of list")

        return True
    return False


def validate_extra_info(extra_info):
    if extra_info:
        if not isinstance(extra_info, list):
            raise Exception("extra_info needs to be a list")

        for extra in extra_info:
            if not isinstance(extra, tuple):
                raise Exception(
                    "extra_info needs to be a tuple: (name, value)")
            yield extra
    return []


def validate_graphene_type(graphene_type):
    if graphene_type:
        if not issubclass(graphene_type, DjangoObjectType):
            raise Exception(
                "graphene_type needs to inherit from DjangoObjectType")
        if not is_valid_django_model(graphene_type._meta.model):
            raise Exception("Meta.model needs to be a valid django model")
        return True
    return False


def get_graphene_arguments(graphene_type, is_required=[]):
    # Accessing specific place in graph type that has all options needed
    graphene_type_options = graphene_type._meta.class_type._meta.__dict__
    # Getting all the fields in the type
    fields = graphene_type_options.get("fields")

    for name, field in fields.items():
        # Creating ExtraArgument instance
        # This object will be returned
        new_argument = ExtraArgument()

        # The field comes from the graphene_type,therefore
        # the display and property name are the same
        new_argument.display_name = name
        new_argument.property_name = name
        # Field comes from the type directly, so it's assumed that is a property
        new_argument.is_property = True

        if field_type := field.__dict__.get("_type"):
            # If it is not a graphene scalar, but a graphene structure like,
            # nonNull, the actual scalar will be inside of the "of_type"
            # key in the structure object.__dict__
            gp_scalar = field_type.__dict__.get("_of_type")

            if gp_scalar:
                new_argument.of_type = gp_scalar
            # If field it's not an structure, then
            # the field is the scalar
            else:
                new_argument.of_type = field_type

        # If the field is a relationship
        elif callable(field.type):
            new_argument.is_relationship = True
            new_argument.of_type = graphene.String

        new_argument.model = graphene_type_options.get("model")

        if name in is_required:
            new_argument.is_required = True

        yield new_argument
