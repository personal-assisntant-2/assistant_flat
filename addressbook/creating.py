''' the functions are helped views.py
    '''
from typing import List
from .models import Abonent, Phone, Email, Note, Tag


def create_phones(abonent: Abonent, out_phones:List[str]):
    ''' add few records to table Phone'''
    for phone in out_phones:
        if phone :
            Phone.objects.create(abonent=abonent,
                                    phone = phone)

def create_emails(abonent: Abonent, out_emails:List[str]):
    ''' add few records to table Email'''
    for email in out_emails:
        if email :
            Email.objects.create(abonent=abonent,
                                    email = email)

def create_note(abonent: Abonent,
                out_note:str,
                in_tags:List[Tag],
                out_tags:List[str]):
    ''' add one record to table Note'''

    if out_note:
        note = Note.objects.create(
            abonent=abonent,
            note=out_note)

        # создаем объекты тегов если их нет в таблице,
        # или получаем их если они в таблице есть
        # и складываем в список, чтобы потом к ним привязать заметку
        #tags_list = []
        for tag_str in out_tags:
            # поле тега может быть пустым, тогда пропускаем его
            if tag_str:
                # записываем объект тэга (найденный или созданный)
                # в список
                tag_obj = Tag.objects.get_or_create(tag=tag_str)[0]
                # связываем все теги с заметкой
                tag_obj.note.add(note)
                