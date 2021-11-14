from django.test import TestCase

from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.urls import reverse



class BaseAddressbookTest(TestCase):
    pass


class TestAuthUser(BaseAddressbookTest):
    client = Client()
    
    def test_register_user(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('register'), 
                    {'username' : 'boss', 
                     'email'    : 'lennon@thebeatles.com',
                    'password1' : '111',
                    'password2' : '111'})
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],'/addressbook/birthdays/')
        
        #вываливалась ошибка . дырка в if  во вьюшке  register
        response = self.client.post(reverse('register'), 
                    {'username' : 'boss', 
                     'email'    : 'lennon@thebeatles.com',
                    'password1' : '111',
                    'password2' : '111'})
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],'/register/')
        
        response = self.client.post(reverse('register'), 
                    {'username' : 'boss', 
                     'email'    : 'lennon@thebeatles.com',
                    'password1' : '111',
                    'password2' : '222'})
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],'/register/')
        

    def test_login_user(self):
        user = User.objects.create_user('boss', 'lennon@thebeatles.com', '111')
        boss = User.objects.get(id= 1)
        response = self.client.post(reverse('login'), {'username' : 'boss', 'password' : '111'})
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'], '/addressbook/birthdays/')
        
        response = self.client.post(reverse('login'), {'username' : 'boss', 'password' : '222'})
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        user = User.objects.create_user('boss', 'lennon@thebeatles.com', '111')
        user_is_auth = authenticate(username='boss', password = '111')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'], '/dashboard/')
    
