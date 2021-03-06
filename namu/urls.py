from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("id/", views.redirect_to_index, name="redirectToIndex"),
    path("id/<int:user_id>/", views.redirect_to_buy, name="redirectToBuy"),
    path("id/<int:user_id>/buy", views.Buy.as_view(), name="buy"),
    path("id/<int:user_id>/topup", views.Topup.as_view(), name="topup"),
    path("id/<int:user_id>/revert", views.revert_previous_transaction, name="revert"),
    path("products/", views.Products.as_view(), name="products"),
    path("stats/", views.statistics, name="stats"),
]
