from django.test import TestCase
import graphene
from mutations.mutation_base import MutationBase
from test_mutations.graphene_django_type import IsolatedModelType, IsolatedModel


class MutationBaseFormatFunctionsTestCase(TestCase):

    def setUp(self):
        self.mutation_base = MutationBase

    def test_format_extra_arguments(self):

        func = self.mutation_base.format_extra_arguments
        # test for emptiness
        gen = func([])
        for i in gen:
            self.assertFalse(i)

        # test for correctness
        correct_name = "c_name"
        gen = func([
            (correct_name, graphene.String())
        ])
        for i in gen:
            self.assertEqual(correct_name, i.display_name)
            self.assertEqual(correct_name, i.property_name)
            self.assertTrue(isinstance(i.of_type, graphene.String))
            self.assertTrue(i.is_property)
            self.assertFalse(i.is_relationship)
            self.assertFalse(i.is_required)

        # test for property false
        is_property_false = False
        gen = func([
            (correct_name, graphene.String(), is_property_false)
        ])
        for i in gen:
            self.assertFalse(i.is_property)

        # test for different display and property name
        names = ("display", "property")
        gen = func([
            (names, graphene.String())
        ])
        for i in gen:
            self.assertEqual(i.display_name, names[0])
            self.assertEqual(i.property_name, names[1])

        # test for is_required
        gen = func([(names, graphene.String())], [names[0]])
        for i in gen:
            self.assertTrue(i.is_required)

    def test_format_graphene_arguments(self):
        func = self.mutation_base.format_graphene_arguments

        # Test fields are being created
        arg_name_in_type = IsolatedModelType().__dict__
        args = func(IsolatedModelType)
        for i in args:
            self.assertTrue(i.display_name in arg_name_in_type)


class MutationBaseSetFunctionsTestCase(TestCase):

    def setUp(self):
        self.mutation_base = MutationBase()

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

