from django.test import TestCase
import graphene
from mutations.validator import Validator
from test_mutations.graphene_django_type import IsolatedModelType


class ValidatorFunctions(TestCase):

    def setUp(self):
        self.validator = Validator

    def test_validate_extra_argument(self):

        func = self.validator.validate_extra_arguments
        self.assertFalse(func(None))

        extra_argument_correct = [
            ("Argument", graphene.String(), True)
        ]
        self.assertTrue(func(extra_argument_correct))

        extra_argument_wrong_scalar = [
            ("Argument", graphene.String)
        ]
        self.assertRaises(Exception, func, extra_argument_wrong_scalar)

        extra_argument_name_invalid_type = [
            (25, graphene.String())
        ]
        self.assertRaises(Exception, func, extra_argument_name_invalid_type)

        extra_argument_wrong_name_format = [
            (("", "", ""), graphene.String())
        ]
        self.assertRaises(Exception, func, extra_argument_wrong_name_format)

        extra_argument_is_property_invalid_type = [
            (("", ""), graphene.String(), None)
        ]
        self.assertRaises(
            Exception, func, extra_argument_is_property_invalid_type)

        extra_arguments_not_a_list = ("Argument", graphene.String(), True)
        self.assertRaises(Exception, func, extra_arguments_not_a_list)

    def test_validate_custom_auth(self):

        func = self.validator.validate_custom_auth
        self.assertFalse(func(None))

        # A function is not passed case
        self.assertRaises(Exception, func, True)

        def correct_auth():
            return (True, [])
        self.assertTrue(func(correct_auth))

        def auth_not_tuple():
            return True
        self.assertRaises(Exception, func, auth_not_tuple)

        def auth_confirmation_not_bool():
            return None, []
        self.assertRaises(Exception, func, auth_confirmation_not_bool)

        def auth_messages_not_list():
            return True, ""
        self.assertRaises(Exception, func, auth_messages_not_list)

    def test_validate_extra_info(self):
        func = self.validator.validate_extra_info
        self.assertFalse(func(None))
        self.assertTrue(func({}))
        self.assertRaises(Exception, func, 25)

    def test_validate_graphene_type(self):
        func = self.validator.validate_graphene_type
        self.assertFalse(func(None))
        self.assertTrue(func(IsolatedModelType))
        self.assertRaises(Exception, func, 25)
    
    def test_validate_mutation_functions(self):
        func = self.validator.validate_mutation_functions
        self.assertRaises(Exception, func, "hey")
        self.assertFalse(func(None))
        def normal_func():
            pass
        self.assertTrue(func(normal_func))
