
'''from django.contrib.auth.decorators import login_required

@login_required 
 @login_required(login_url='auth:login')
'''
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .forms import AbonentEditForm, FindContactsForm
from .models import Abonent, Phone, Email, Note, Tag
from .queries import read_abonents, get_date_month_day
from .creating import create_phones, create_emails, create_note
from .updating import update_phones, update_emails

from datetime import date, timedelta


class AbonentDetailView(DetailView):
    """built-in view
        to view one contact from model Abonent
        data from Phone, Email, Note are added to the standard context
    """
    model = Abonent
    #template_name = 'addressbook/detail.html'
    context_object_name = 'abonent'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['phones'] = Phone.objects.filter(
            abonent_id=context['abonent'].id)
        context['emails'] = Email.objects.filter(
            abonent_id=context['abonent'].id)
        context['notes'] = Note.objects.filter(
            abonent_id=context['abonent'].id)
        print('------list-', context)
        return context

@login_required
def add_contact(request):
    ''' form for adding a contact
     there are all fields from all models.
     name
     birthday
     address
     phone - 3
     email - 3
     the note
     tag - 2
     records are manually created in all tables.
     validation not registered yet
    '''
    # список тегов нужен для автозаполнения(подсказки) в поле тегов
    tags = Tag.objects.all()
    context = {'tags': [tag.tag for tag in tags]}
    if request.method == 'POST':
        # считываем данные с реквеста и сразу записываем в словарь
        # иначе теряются телефоны, и почты, остается только один, из последного поля
        data = dict(request.POST)
        # если нет имени, форма возвращается пустая
        if not data['name'][0]:
            return redirect(reverse('addressbook:add-contact'))

        # создается запись в Аbonent
        abonent = Abonent.objects.create(
            owner_id=request.user.id,
            name=data['name'][0],
            birthday=data['birthday'][0],
            address=data['address'][0])
        
        # создаются записи в Phone
        create_phones(abonent=abonent,
                    out_phones=data['phone'] )
        
        # создаются записи в Email
        create_emails(abonent=abonent,
                    out_emails=data['email'] )
        
        # Добавляем заметку в таблицу  Note
        create_note(abonent=abonent,
                        out_note=data['note'][0], 
                        in_tags=context['tags'],
                        out_tags=data['tag']  )

        return redirect(reverse('addressbook:detail', kwargs= {'pk' : abonent.id }))
    
    return render(request, 'addressbook/add_contact.html', context)

@login_required
def edit_contact(request, pk):
    ''' Edit contact
    possible :  change name
                change address
                delete address
                change birthday
                add new phone
                change phone
                delete phone
                add new email
                change email
                delete email
                add new note
    '''
    context = {}
    context['abonent'] = Abonent.objects.get(id=pk)
    context['phones'] = Phone.objects.filter(abonent_id=pk)
    context['emails'] = Email.objects.filter(abonent_id=pk)
    print('________', context)
    # список тегов нужен для автозаполнения(подсказки) в поле тегов
    tags = Tag.objects.all()
    context['tags'] = [tag.tag for tag in tags]
    if request.method == 'POST':
        # считываем данные с реквеста и сразу записываем в словарь
        # иначе теряются телефоны, и почты, остается только один, из последного поля
        data = dict(request.POST)
        print(data)
        # если нет имени, форма возвращается пустая
        if not data['name'][0]:
            return redirect(reverse('addressbook:edit-contact'))
        
        # апдейтится запись в Аbonent
        
        Abonent.objects.update_or_create(id = pk, defaults = {
                              'name': data['name'][0],
                              'birthday': data['birthday'][0],
                              'address': data['address'][0]})
        
        # апдейтятся записи в Phone
        update_phones(abonent=context['abonent'],
                    in_phones=context['phones'], 
                    out_phones=data.get('phone', []) )
        
        # создание нового телефона из списка new_phone
        create_phones(abonent=context['abonent'],
                    out_phones=data['new_phone'] )

        # апдейтятся записи в Email
        update_emails(abonent=context['abonent'],
                    in_emails=context['emails'], 
                    out_emails=data.get('email',[]) )
        
         # создание нового email  из списка new_email
        create_emails(abonent=context['abonent'],
                    out_emails=data['new_email'] )
        
        # Добавляем заметку в таблицу  Note
        create_note(abonent=context['abonent'],
                        out_note=data['note'][0], 
                        in_tags=context['tags'],
                        out_tags=data['tag']  )
        print(1)
        return redirect(reverse('addressbook:detail', kwargs= {'pk' : context['abonent'].id }))
    print(2, '!!!!!!',context)
    return render(request, "addressbook/edit_contact.html", context)

@login_required
def delete_contact(request, pk):
    ''' only delete one abonent from Abonent
    reaction by press button in temaplate 'abonent_datail'
    '''
    abonent = Abonent.objects.get(id=pk)
    abonent.delete()
    return redirect(reverse('addressbook:home'))

@login_required
def birthdays(request, period=50):

    '''The first page  after authentication.
    There will be list of friends, 
    who has birthday in the near future
    ordered
    '''
    # даты будут сравниваться как кортежи (месяц, день)
    abonents_list = get_date_month_day(period, owner = request.user)
    
    content = { 'abonents': abonents_list,  }

    return render(request, 'addressbook/birthdays.html', content)

@login_required
def home(request):
    ''' The first page of Addressbook
    List of all contacts of user
    '''
    all_abonent = Abonent.objects.filter(owner=request.user)
    content = {
        'abonents': all_abonent,
    }
    return render(request, 'addressbook/home.html', content)


@login_required()
def find_contacts(request):
    """предоставляет форму ввода, в которую можно ввести следующие поисковые атрибуты:
    - паттерн (поиск совпадения по всем текстовым полям (имя, адрес, телефон, email, note)),
    - даты (при поиске учитывает даты рождения и даты создания заметок). Варианты поиска:
        - совпадение с конкретной датой
        - до какой-то даты (включая ее)
        - после какой-то даты (включая ее)
        - между какими-то датами (включая эти даты)
    - тэги (при поиске просматирваются поля "tag" привязанные к note)
    Если при поиске введено несколько поисковых атрибутов, то модель 
    поиска "<атрибут 1> and <атрибут 2> and <атрибут 3>"
    Результат поиска в виде списка соовествующих записей в кратком представлении 
    (каждая запись - ссылка, при нажатии на которую осуществляется переход на страницу 
    записи с детальной информацией)
    """
    if request.method == 'POST':
        form = FindContactsForm(request.POST)
        if form.is_valid():
            res = form.cleaned_data
            user = request.user
            print('user: ', user)
            abonents = read_abonents(user,
                                     pattern=res['pattern'], tags=res['tags'], date_start=res['date_start'], date_stop=res['date_stop'])
            print(abonents)

            content = {'form': form, 'abonents': abonents}
            return render(request, "addressbook/find-contacts.html", content)
    else:
        form = FindContactsForm()

    return render(request, "addressbook/find-contacts.html", {'form': form})
