from django.test import TestCase
from ..models import IsolatedModel
from ..schema import schema


class DeleteMutationTests(TestCase):

    def setUp(self):
        first_isolated = IsolatedModel(
            integer_field=25,
            char_field="Some Random String",
            float_field=255.6,
            decimal_field=56.6,
        )
        first_isolated.save()

        second_isolated = IsolatedModel(
            integer_field=26,
            char_field="Some Random String",
            float_field=255.6,
            decimal_field=56.6,
        )
        second_isolated.save()

        third_isolated = IsolatedModel(
            integer_field=27,
            char_field="Some Random String",
            float_field=255.6,
            decimal_field=56.6,
        )
        third_isolated.save()

    def test_delete_elements(self):
        # Check if entries exists
        self.assertTrue(IsolatedModel.objects.get(id=1))
        self.assertTrue(IsolatedModel.objects.get(id=2))
        self.assertTrue(IsolatedModel.objects.get(id=3))
        
        # Deleting entry with id 1
        one_delete_result = schema.execute(
            '''
                mutation{
                  deleteIsolatedType(id:1){
                    completed,
                    messages
                  }
                }
            '''
        ).data.get("deleteIsolatedType")

        many_delete_result = schema.execute(
            '''
                mutation{
                  deleteIsolatedType(id:[2, 3]){
                    completed,
                    messages
                  }
                }
            '''
        ).data.get("deleteIsolatedType")
        

        # Check if mutations returns what is expected
        self.assertTrue(one_delete_result.get("completed"))
        self.assertIsNone(one_delete_result.get("messages"))
        self.assertTrue(many_delete_result.get("completed"))
        self.assertIsNone(many_delete_result.get("messages"))


        # Check if entry no longer exist
        self.assertRaises(Exception, IsolatedModel.objects.get, id=1)
        self.assertRaises(Exception, IsolatedModel.objects.get, id=2)
        self.assertRaises(Exception, IsolatedModel.objects.get, id=3)


