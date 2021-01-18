from django.test import TestCase
import graphene
from mutations.mutation_argument import MutationArgument


class MutationArgumentSetFunctionsTestCase(TestCase):

    def setUp(self):
        self.arg = MutationArgument(
            display_name="name",
            property_name="prop_name",
            graphene_scalar=graphene.Int()
        )

    def test_display_name_is_empty_or_none(self):

        # Test for fail cases
        self.assertRaises(Exception, self.arg.set_display_name, " ")
        self.assertRaises(Exception, self.arg.set_display_name, None)

        self.assertRaises(Exception, self.arg.set_property_name, " ")
        self.assertRaises(Exception, self.arg.set_property_name, None)

        # Test for correctness
        self.arg.set_display_name("display one")
        self.assertEqual("display one", self.arg.display_name)

        self.arg.set_property_name("property one")
        self.assertEqual("property one", self.arg.property_name)

    def test_graphene_scalar_is_correct_type(self):

        self.assertRaises(Exception, self.arg.set_of_type, graphene.String)
        self.assertRaises(Exception, self.arg.set_of_type, None)
        self.assertRaises(Exception, self.arg.set_of_type, "")
