from django.test import TestCase, Client
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.urls import reverse

from ..models import Abonent, Phone, Email, Note, Tag



class BaseAddressbookTest(TestCase):
    pass
'''
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
        print(response.headers)
        self.assertURLEqual(
            response.headers['Location'],'/addressbook/birthdays/')
        
        #  вываливалась ошибка . дырка в if  во вьюшке  register
        response = self.client.post(reverse('register'), 
                    {'username' : 'boss', 
                     'email'    : 'lennon@thebeatles.com',
                    'password1' : '111',
                    'password2' : '111'})
        print(response.status_code)
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post(reverse('register'), 
                    {'username' : 'boss', 
                     'email'    : 'lennon@thebeatles.com',
                    'password1' : '111',
                    'password2' : '222'})
        print(response.status_code)
        self.assertEqual(response.status_code, 302)
        
        
    def test_redirect(self):
        response = self.client.post(reverse('addressbook:home'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],
            reverse('login') + '?next=/addressbook/home/'
        )

    def test_login_user(self):
        user = User.objects.create_user('boss', 'lennon@thebeatles.com', '111')
        boss = User.objects.get(id= 1)
        response = self.client.post(reverse('login'), {'username' : 'boss', 'password' : '111'})
        print('-----login-----',response.headers)
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

'''
class TestViewFormEdit(BaseAddressbookTest):
    pass

class TestFormEdit(BaseAddressbookTest):

    def setUp(self):
        super().setUp()
        user = User.objects.create_user('boss', 'lennon@thebeatles.com', '111')

        user_is_auth = authenticate(username='boss', password = '111')
        #print('-------',type(user), type(user_is_auth))
        self.path = reverse('addressbook:edit-contact')
        abonent = Abonent(owner = user,
                name = 'Joe',
                address = 'NewYork',
                birthday = '2002-05-09')
        abonent.save()
        print('------abonent------', abonent)
        self.response = self.client.get(self.path)
        
        phones = []
        for elem in ['1122','1133','1144']:
            phone = Phone(abonent = abonent, phone = elem)
            phone.save()
            phones.append(phone)
        
        emails = []
        for elem in ['joe@joe.joe','joe@.com']:
            email = Email(abonent = abonent, email = elem)
            email.save()
            emails.append(email)

        note = Note(abonent = abonent, note = 'bignote')
        note.save()
        tag = Tag(note=note, tag = 'bigtag')
        tag.save()
        tag.note.add(note)

    def test_open_page_edit(self):
        self.assertEqual(self.response.status_code, 200)

    def test_change_name(self):
        request = self.factory.post(self.path, context)
        print(request)
        abonent = Abonent.objects.first()
        self.assertEqual(request.POST['name'], abonent.name)
