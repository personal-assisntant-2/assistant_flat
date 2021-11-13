from django.test import TestCase

from .models import Abonent, Phone, Email, Note, Tag

class BaseAddressbookTest(TestCase):
    factory = RequestFactory()

class TestFormCreateAbonent(BaseAddressTest):
    pass



class TestFormEditAbonent(BaseAddressTest):

    def setUp(self):
        super().setUp()
        abonent = Abonent(owner = self.client.get(),
                name = 'Joe',
                address = 'NewYork',
                birthday = '2002-05-09')
        abonent.save()
        self.path = reverse('addressbook:edit-contact')
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
        