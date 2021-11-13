from typing import List
from .models import Abonent, Phone, Email, Note, Tag


def create_phones(abonent: Abonent, out_phones:List[str]):
    for phone in out_phones:
        if phone :
            Phone.objects.create(abonent=abonent,
                                    phone = phone)
    

def create_emails(abonent: Abonent, out_emails:List[str]):
    for email in out_emails:
        if email :
            Email.objects.create(abonent=abonent,
                                    email = email)

def create_note(abonent: Abonent, 
                out_note:str, 
                in_tags:List[Tag],
                out_tags:List[str]):

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
                    '''
                    if tag not in in_tags:
                        tags_list.append(Tag.objects.create(tag=tag))
                    else:
                        # если такой тег есть в таблице, то находим его и запоминаем
                        # чтобы потом с ним связать заметку
                        tag = Tag.objects.get(tag=tag)
                        tags_list.append(tag)
                    '''
            '''
            # связываем все теги с заметкой
            for tag in tags_list:
                tag.note.add(note)
            '''