from django.test import TestCase
import graphene
from mutations.mutation_base import MutationBase
from test_mutations.graphene_django_type import RelationshipReceiverModelType, IsolatedModelType


class MutationBaseSetFunctionsTestCase(TestCase):

    def setUp(self):
        self.mutation_base = MutationBase()
        self.mutation_base_second = MutationBase()

    def test_set_graphene_type(self):

        options = {
            "graphene_type": IsolatedModelType
        }
        self.mutation_base.set_graphene_type(options)
        self.assertTrue(issubclass(
            self.mutation_base.graphene_type, IsolatedModelType))

    def test_set_arguments(self):
        # Setting the arguments
        options = {
            "extra_arguments" : [("ext_arg", graphene.String())],
            "graphene_type" : IsolatedModelType
        }
        self.mutation_base.set_arguments(options)

        # Testing for arguments in graphene_type
        arg_name_in_type = IsolatedModelType().__dict__
        for arg in arg_name_in_type:
            self.assertTrue(hasattr(self.mutation_base.Arguments, arg))

        # Testing for extra_arguments
        ext_args = options.get("extra_arguments")
        for arg in ext_args:
            self.assertTrue(hasattr(self.mutation_base.Arguments, arg[0]))
        
        # Checking for leakage
        empty_options = {
            "graphene_type" : RelationshipReceiverModelType,
            "extra_arguments" : []
        }
        self.mutation_base_second.set_arguments(empty_options)

        for arg in arg_name_in_type:
            if not arg == "name" and not arg =="id":
                self.assertFalse(hasattr(self.mutation_base_second.Arguments, arg))

        for arg in ext_args:
            self.assertFalse(hasattr(self.mutation_base_second.Arguments, arg[0]))

