from django import forms
from datetime import date
from .models import Abonent, Tag


class AbonentForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    birthday = forms.DateField(
        label='день рождения', widget=forms.widgets.SelectDateWidget())
    #email = forms.EmailField(label='электронная очта', widget=forms.widgets.EmailInput())

    class Meta:
        model = Abonent
        fields = ('name', 'birthday')  # , 'email')

class AbonentEditForm(forms.Form):
    name = forms.CharField(label = 'Имя')
    birthday = forms.DateField(
    label='день рождения', widget=forms.widgets.SelectDateWidget())
    address = forms.CharField(label = "Адрес")
    email = forms.EmailField(label='электронная почта', widget=forms.widgets.EmailInput())
    

class FindContactsForm(forms.Form):
    year_max = date.today().year + 1
    # tags_dict = {elem.tag: elem for elem in Tag.objects.all()}
    tags_test = [(tag.tag, tag.tag) for tag in Tag.objects.all()]
    #tags_test = [('A', 'a'), ('B', 'b'), ('C', 'c')]
    pattern = forms.CharField(label='паттерн', required=False,
                              help_text='набор символов, которым будет искаться соотвествие (в имени, тпелефонах, адресах, email, заметках)')
    tags = forms.MultipleChoiceField(
        choices=tags_test, widget=forms.CheckboxSelectMultiple, label='выберите тэги', required=False, help_text='можно выбрать один или несколько тэгов, по которым будет осуществляться поиск')
    date_start = forms.DateField(label='дата старт', widget=forms.SelectDateWidget(
        years=[a for a in range(year_max - 90, year_max)]), required=False)
    date_stop = forms.DateField(label='дата стоп', widget=forms.SelectDateWidget(
        years=[a for a in range(year_max - 90, year_max)]), required=False)
