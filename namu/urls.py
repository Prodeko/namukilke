from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    #path('id/<int_userid>/'), redirect('id/<int_userid/buy'),
    path('id/<int:user_id>/buy', views.Buy.as_view(), name='buy'),
    path('id/<int:user_id>/deposit', views.Deposit.as_view(), name='deposit'),
]
