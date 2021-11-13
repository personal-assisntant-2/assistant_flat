from django.urls import path

from . import views


app_name = 'news'

urlpatterns = [
    path('', views.new_view, name='news'),
    ]
