from django.urls import include, path
from .views import dashboard, register

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', dashboard, name="dashboard"),
    path('dashboard/', dashboard, name="dashboard"),
    
    path('register/', register, name="register"),
]
