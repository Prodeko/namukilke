from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('id/', views.redirectToIndex, name='redirectToIndex'),
    path('id/<int:user_id>/', views.redirectToBuy, name='redirectToBuy'),
    path('id/<int:user_id>/buy', views.Buy.as_view(), name='buy'),
    path('id/<int:user_id>/deposit', views.Deposit.as_view(), name='deposit'),
]