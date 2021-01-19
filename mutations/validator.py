from types import FunctionType
from graphene import Scalar
from graphene_django import DjangoObjectType
from graphene_django.utils.utils import is_valid_django_model


class Validator():
    def validate_extra_arguments(extra_arguments: list) -> bool:
        if extra_arguments:
            if not isinstance(extra_arguments, list):
                raise Exception("extra_arguments needs to be a list")

            for argument in extra_arguments:
                if not isinstance(argument, tuple):
                    raise Exception(
                        "extra_arguments needs to be a tuple: (names, graphene_type, is_property)")

                if isinstance(argument[0], tuple):
                    for i in range(len(argument[0])):
                        if i > 1:
                            raise Exception(
                                "name tuple only take two arguments")
                        if not isinstance(argument[0][i], str):
                            raise Exception(
                                "extra_argument name needs to be a str")
                elif not isinstance(argument[0], str):
                    raise Exception("extra_argument name needs to be a str")

                if not isinstance(argument[1], Scalar):
                    raise Exception(
                        "extra_arguments second value in tuple needs to be an instance of scalar")
                # If argument has is_property
                if len(argument) >= 3:
                    if not isinstance(argument[2], bool):
                        raise Exception(
                            "extras arguments third value in tuple needs to be a bool")
            return True
        return False

    def validate_custom_auth(custom_auth: FunctionType) -> bool:
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

    def validate_extra_info(extra_info: list) -> bool:
        if isinstance(extra_info, dict):
            return True
        if extra_info:
            raise Exception("extra info needs to be an instance of dict")

        return False

    def validate_graphene_type(graphene_type: DjangoObjectType) -> bool:
        if graphene_type:
            if not issubclass(graphene_type, DjangoObjectType):
                raise Exception(
                    "graphene_type needs to inherit from DjangoObjectType")
            if not is_valid_django_model(graphene_type._meta.model):
                raise Exception("Meta.model needs to be a valid django model")
            return True
        return False
    
    def validate_mutation_functions(before_mutate) -> bool:
        if before_mutate:
            if callable(before_mutate):
                return True
            raise Exception("before_mutate needs to be a function")
        return False
