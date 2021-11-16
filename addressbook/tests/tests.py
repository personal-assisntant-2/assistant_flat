''' tests for addressbook'''

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

#from django.test.client import RequestFactory
#from django.contrib.auth import authenticate, get_user

from ..models import Abonent, Phone, Email, Note, Tag

#проверить что пользователь успешно вошел в систему
#user = get_user(client)
#user.is_authenticated


class BaseAddressbookTest(TestCase):
    '''fish'''

class TestFormEdit(BaseAddressbookTest):
    ''' tests page edit-contact '''

    def setUp(self):
        ''' prepare data for  page edit-contact'''
        super().setUp()
        user = User.objects.create_user('boss', 'lennon@thebeatles.com', '111')

        #user_is_auth = authenticate(username='boss', password = '111')
        print('auth?-----',user.is_authenticated)
        #print('-------',type(user), type(user_is_auth))
        abonent = Abonent(owner = user,
                name = 'Joe',
                address = 'NewYork',
                birthday = '2002-05-09')
        abonent.save()
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
        tag = Tag(tag = 'bigtag')
        tag.save()
        tag.note.add(note)

        self.context = {}
        self.context['abonent'] = Abonent.objects.get(id=abonent.id)
        self.context['phones'] = Phone.objects.filter(abonent_id=abonent.id)
        self.context['emails'] = Email.objects.filter(abonent_id=abonent.id)
        tags = Tag.objects.all()
        self.context['tags'] = [tag.tag for tag in tags]

    def test_open_page_edit(self):
        '''for page edit-contact. is open ? '''
        abonent = Abonent.objects.first()
        path = reverse('addressbook:edit-contact', kwargs= {'pk' : abonent.id })
        #print('------path------', path)
        response = self.client.get(path)
        print('----response---',response.context)
        #print('---resp.request----', response.request)
        #print('---resp.headers----', response.headers)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            f'/accounts/login/?next=/addressbook/edit_contact/{abonent.id}/')
'''
    def test_input_fields(self):
        abonent = Abonent.objects.first()
        print(self.context)
        response = self.client.get(reverse("addressbook:edit-contact",kwargs= {'pk' : abonent.id }))
        print('---input---', response.request)
        #response = self.client.get("/addressbook/edit_contact/")
        #print('---input---', response)
        
        self.assertEqual(response.context['abonent'].name, 'Joe')

    def test_change_name(self):
        abonent = Abonent.objects.first()
        print(abonent.id)
        response = self.client.post(reverse('addressbook:edit-contact', 
                kwargs= {'pk' : abonent.id }), {'name' : 'no boss'})
        print('---resp.request----', response.context)
        abonent = Abonent.objects.get(id = abonent.id)
        self.assertEqual(abonent.name, "no boss")
'''