''' the functions are hepled views.py
'''
from typing import List, Dict

from datetime import date, timedelta
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Abonent

# , date_min: date = None, date_max: date = None


def read_abonents(user, pattern: str = '', tags: list = [],
                    date_start: date = None, date_stop: date = None) -> list:
    """Ищет и возвращает список экземпляров записей типа Abonent,
    соотвествующих параметрам поиска.
    Параметры поиска задаются паттерном 'pattern', списком tags и
    временным интервалом date_min ... date_max.
    Если  pattern == '' (пустая строка - состояние по умолчанию),
    поиск осуществляется только с учетом
    остальных параметров. Поиск по паттерну проходит по всем
    текстовым и строковым полям БД: name,
    address, phone, email, note.
    Поиск по временным отметкам осуществляется по полям
    Abonent.birthday и Note.date (дата создания заметки)
    Поиск по временным отметкам реализуется по правилам:
    - date_min == None and date_max == None - состояние по умолчанию.
    Поиск по времени не осуществляется.
    - date_min == None and date_max == date - в результаты поиска
    включаются записи, временные отметки которых
    соотвествуют условию < date_max
    - date_min == date and date_max == None -  в результаты поиска
    включаются записи, временные отметки которых
    соотвествуют условию > date_min
    - date_min == date_1 and date_max == date_2 -  в результаты поиска
    включаются записи, временные отметки которых
    соотвествуют условию BETWEEN date_1 AND date_2 (попадающие в интервал,
    включая границы)
    - date_min == date_max (тип данных - date) - в выборку попадут записи
    в которых временные метки равны date_min
    """
    if pattern == '':
        results_patt = Abonent.objects.filter(owner=user)
    else:
        #results_patt = Abonent.objects.filter(emails__email__icontains=pattern)
        results = Abonent.objects.filter(owner=user)
        results_patt = results.filter(name__icontains=pattern)

        r1 = results.filter(address__icontains=pattern)
        r2 = results.filter(notes__note__icontains=pattern)
        r3 = results.filter(phones__phone__icontains=pattern)
        r4 = results.filter(emails__email__icontains=pattern)

        results_patt.union(r1, r2, r3, r4)
    if tags == []:
        results_patt_tags = results_patt
    else:
        #results_patt_tags = results_patt &
        # Abonent.objects.filter(notes__tags__tag=tags[0])
        results_patt_tags = results_patt.filter(notes__tags__tag=tags[0])

        for t in tags[1:len(tags)]:
            results_patt_tags = results_patt_tags.filter(notes__tags__tag=t)
            # & Abonent.objects.filter(notes__tags__tag=t)

    if date_start is None and date_stop is None:
        results_patt_tags_date = results_patt_tags
    elif date_start is not None and date_stop is None:
        results_patt_tags_date_birthday = results_patt_tags.filter(
            birthday__gte=date_start)
        results_patt_tags_date_notes = results_patt_tags.filter(
            notes__date__gte=date_start)
        results_patt_tags_date = results_patt_tags_date_birthday.union(
            results_patt_tags_date_notes)
    elif date_start is None and date_stop is not None:
        results_patt_tags_date_birthday = results_patt_tags.filter(
            birthday__lte=date_stop)
        results_patt_tags_date_notes = results_patt_tags.filter(
            notes__date__lte=date_stop)
        results_patt_tags_date = results_patt_tags_date_birthday.union(
            results_patt_tags_date_notes)
    else:
        results_patt_tags_date_birthday = results_patt_tags.filter(
            birthday__lte=date_stop) & results_patt_tags.filter(
            birthday__gte=date_start)

        results_patt_tags_date_notes = results_patt_tags.filter(
            notes__date__lte=date_stop) & results_patt_tags.filter(
            notes__date__gte=date_start)
        results_patt_tags_date = results_patt_tags_date_birthday.union(
            results_patt_tags_date_notes)

    return results_patt_tags_date

def get_date_month_day(period : int, owner)->List[Dict]:
    ''' query abonenets by date in the range
    from today to plus "period" days
    dates will compared as tuples(month , day)
    '''
    def check_bd_between(bd:List[int],begin:List[int], end:List[int]):
        return begin < bd < end
    # даты будут сравниваться как кортежи (месяц, день)
    begin = date.today()
    end = begin + timedelta(days=period)
    print(begin)
    print(end)
    abonents = Abonent.objects.filter(owner=owner,
                                       birthday__isnull=False)
    abonents_list = []
    #  из полученного полного запроса переписываются в список только подходящие
    for abonent in abonents:
        date_begin = [begin.month, begin.day]
        date_end = [end.month, end.day]
        bd = [abonent.birthday.month, abonent.birthday.day]
        birthday_isbetween = False
        if  date_begin[0] <= date_end[0] :
            birthday_isbetween = check_bd_between(bd, date_begin, date_end)
        else:
            date_end[0] += 12
            birthday_isbetween = check_bd_between(bd, date_begin, date_end)
            if not birthday_isbetween:
                bd[0] += 12
                birthday_isbetween = check_bd_between(bd, date_begin, date_end)
        if  birthday_isbetween:
            abonents_list.append({'pk': abonent.id,
                                'name': abonent.name,
                                'birthday': abonent.birthday,
                                'short_bd': bd,
                                'str_bd': abonent.birthday.strftime('%A %d %B %Y')})
    # сортировка по (месяц, день)
    abonents_list.sort(key=lambda el: el['short_bd'])
    return abonents_list


def invalid_emails(request, context: dict):
    """
    Checks the validity of the email,
    if the validation is successful it returns None, and if it fails - None.
    """
    f = forms.EmailField()
    print('.....context)', context)
    try:
        if context.get('email'):
            for email in context['email']:
                if email:
                    f.clean(email)

        # если добавлен новый email, вернется list с этим элементом
        new_email = context.get('new_email')
        print('!!!!!!!!!new_email', new_email)

        if new_email:
            if new_email[0]:
                f.clean(new_email[0])

    except ValidationError:
        messages.add_message(request, messages.ERROR, 'Enter a valid email address.')
        return True

    return False
