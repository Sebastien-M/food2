from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy


class ViewsTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(ViewsTestCase, self).__init__(*args, **kwargs)
        self.client = Client()

    def setUp(self):
        User.objects.create(username='test',
                            email='mail@test.com',
                            password='123')

    def test_recipe_detail_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('recipe-detail', kwargs={'pk': 1}), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_daily_recipe_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('daily-recipe'), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_daily_recipe_delete_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('daily-recipe-delete', kwargs={'pk': 1}), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_week_menu_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('week-menu'), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_define_recipe_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('define-recipe'), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_shopping_list_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('shopping-list'), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_shopping_list_update_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('shopping-list-item-update', kwargs={'pk': 1}), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_shopping_list_delete_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('shopping-list-item-delete', kwargs={'pk': 1}), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))

    def test_shopping_list_create_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('shopping-list-item-create'), follow=True)
        # redirection lo signin view when not logged in
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], reverse_lazy('signin'))
