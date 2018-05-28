from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('id/<int:pk>/', views.user, name='user'),
    path('id/<int:user_id>/buy', views.Buy.as_view(), name='buy'), #<-- tälleen tehään eikä pelkkä pk
    path('id/<int:pk>/deposit', views.Deposit.as_view(), name='deposit'),
]
