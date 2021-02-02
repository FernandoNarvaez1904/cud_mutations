from django.test import TestCase
import graphene
from mutations.mutation_base import MutationBase
from ..models import IsolatedModel
from test_mutations.graphene_django_type import IsolatedModelType


class MutationBaseSetFunctionsTestCase(TestCase):

    def setUp(self):
        self.mutation_base = MutationBase
        self.mutation_base_second = MutationBase

    def test_set_graphene_type(self):

        options = {
            "graphene_type": IsolatedModelType
        }
        self.mutation_base.set_graphene_type(self.mutation_base, options)
        self.assertTrue(issubclass(
            self.mutation_base.graphene_type, IsolatedModelType))

    def test_set_graphene_arguments(self):
        # Setting the arguments
        options = {
            "graphene_type": IsolatedModelType
        }
        self.mutation_base.set_graphene_arguments(self.mutation_base, options)

        # Testing for arguments in graphene_type
        arg_name_in_type = IsolatedModelType().__dict__
        for arg in arg_name_in_type:
            self.assertTrue(hasattr(self.mutation_base.Arguments, arg))

    def test_set_extra_arguments(self):
        options = {
            "extra_arguments": [("ext_arg", graphene.String())],
        }
        self.mutation_base.set_extra_arguments(self.mutation_base, options)

        # Testing for extra_arguments
        ext_args = options.get("extra_arguments")
        for arg in ext_args:
            self.assertTrue(hasattr(self.mutation_base.Arguments, arg[0]))

    def test_get_model(self):
        options = {
            "graphene_type": IsolatedModelType
        }
        self.mutation_base.set_graphene_type(self.mutation_base, options)
        self.assertEqual(
            IsolatedModel, self.mutation_base.get_model(self.mutation_base))

    def test_set_extra_info(self):
        options = {
            "extra_info": {
                "prove": 1
            }
        }
        self.mutation_base.set_extra_info(self.mutation_base, options)

        self.assertEqual(options.get("extra_info"),
                         self.mutation_base.extra_info)

    def test_custom_auth(self):

        def auth():
            return (False, [])

        options = {
            "custom_auth": auth
        }
        self.mutation_base.set_custom_auth(self.mutation_base, options)

        ret = self.mutation_base.custom_auth()
        self.assertEqual(auth(), ret)

    def test_set_before_mutate(self):
        self.mutation_base.set_before_mutate(self.mutation_base, {})
        should_be_none = self.mutation_base.before_mutate()
        self.assertIsNone(should_be_none)

        def is_int_25():
            return 25
        self.mutation_base.set_before_mutate(
            self.mutation_base, {"before_mutate": is_int_25})
        should_be_25 = self.mutation_base.before_mutate()
        self.assertEqual(should_be_25, 25)

    def test_set_after_mutate(self):
        self.mutation_base.set_after_mutate(self.mutation_base, {})
        should_be_none = self.mutation_base.after_mutate()
        self.assertIsNone(should_be_none)

        def is_int_25():
            return 25
        self.mutation_base.set_after_mutate(
            self.mutation_base, {"after_mutate": is_int_25})
        should_be_25 = self.mutation_base.after_mutate()
        self.assertEqual(should_be_25, 25)

    def test_set_mutate_method(self):
        self.assertRaises(Exception, self.mutation_base.set_mutate_method)
        self.assertRaises(
            Exception, self.mutation_base.set_mutate_method, "Not a function")

        def is_int_25():
            return 25
        self.mutation_base.set_mutate_method(self.mutation_base, is_int_25)
        should_be_25 = self.mutation_base.mutate_method()
        self.assertEqual(should_be_25, 25)
