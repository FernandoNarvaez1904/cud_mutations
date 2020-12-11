from django.test import TestCase
import graphene
from  API.cud_mutations.extra_argument import ExtraArgument

class CreateExtraArgumentTestCase(TestCase):
    
    def test_display_name_is_empty_or_none(self):
        arg = ExtraArgument(
            display_name="name",
            property_name="prop_name",
            graphene_scalar= graphene.Int
        )
        # Test for fail cases
        self.assertRaises(Exception, arg.set_display_name, " ")
        self.assertRaises(Exception, arg.set_display_name, None)

        # Test for correctness
        arg.set_display_name("name one")
        self.assertEquals("name one", arg.display_name)

    def test_property_name_is_empty_or_none(self):
        arg = ExtraArgument(
            display_name="name",
            property_name="prop_name",
            graphene_scalar= graphene.Int
        )
        # Test for fail cases
        self.assertRaises(Exception, arg.set_property_name, " ")
        self.assertRaises(Exception, arg.set_property_name, None)

        # Test for correctness
        arg.set_property_name("name one")
        self.assertEquals("name one", arg.property_name)



        