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

        self.mutation_base.set_graphene_type(IsolatedModelType)
        
        self.assertTrue(issubclass(self.mutation_base.graphene_type, IsolatedModelType))
