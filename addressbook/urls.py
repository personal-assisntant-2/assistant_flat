
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'addressbook'
urlpatterns = [
    path('add_contact/', views.add_contact, name = 'add-contact'),
    path('delete_contact/<int:pk>/', views.delete_contact, name='delete-contact'),
    path('find-contacts/', views.find_contacts, name='find-contacts'),
    path('home/', views.home, name = 'home'),
    path('detail/<int:pk>/', views.AbonentDetailView.as_view(), name='detail'),
    path('edit_contact/<int:pk>/', views.edit_contact, name='edit-contact'),
    path('add_note/<int:pk>/', views.add_note, name='add-note'),
    path('birthdays/', views.birthdays, name = 'birthdays'),
]
