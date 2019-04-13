""" Created by Oleksandr Sorocynskyi """
""" On 03/04/2019 """

from django.test import TestCase, Client
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
)
from cookbox_core.tests import RecipeBaseTest

class WebuiBaseTest(RecipeBaseTest):
    '''
    Authenticates the client and adds a .client member variable.
    This is done in setUp.
    Remember to call super(...).setUp() after overriding.
    '''

    user = "testuser123"
    user_pswrd = "password123"

    def setUp(self):
        super(WebuiBaseTest, self).setUp()

        user = User.objects.create(username=self.user)
        user.set_password(self.user_pswrd)
        user.save()

        self.client = Client()
        self.client.login(username=self.user,
                          password=self.user_pswrd)


class CreateViewTest(WebuiBaseTest):

    def test_get_200(self):
        # Issue a GET request.
        response = self.client.get(reverse('recipe-create'))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        