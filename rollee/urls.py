from django.urls import path
from . import views

urlpatterns = [
    path('login_and_get_accounts', views.accounts_list),
]
