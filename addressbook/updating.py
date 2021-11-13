from typing import List
from .models import Abonent, Phone, Email, Note, Tag


def update_phones(abonent: Abonent, 
                in_phones:List[Phone], 
                out_phones:List[str]):
    print(in_phones, out_phones)
    for i, phone in enumerate(in_phones):
                if out_phones[i] :
                    if out_phones[i] != phone.phone :
                        Phone.objects.update_or_create(id = phone.id, 
                                        defaults = 
                                        {'abonent': abonent,
                                        'phone' : out_phones[i]})
                else:
                    #если поле ввода оказалось пустым, то значит его удалили
                    # удаляем эту запись из таблицы по id
                    el = Phone.objects.get(id = phone.id)
                    el.delete()
        

def update_emails(abonent: Abonent, 
                in_emails:List[Email], 
                out_emails:List[str]):

    for i, email in enumerate(in_emails):
                if out_emails[i] :
                    if out_emails[i] != email.email :
                        Email.objects.update_or_create(id = email.id, 
                                        defaults = 
                                        {'abonent': abonent,
                                        'email' : out_emails[i]})
                else:
                    #если поле ввода оказалось пустым, то значит его удалили
                    # удаляем эту запись из таблицы по id
                    el = Email.objects.get(id = email.id)
                    el.delete()
