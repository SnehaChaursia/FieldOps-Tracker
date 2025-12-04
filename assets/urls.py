from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Asset CRUD
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", views.asset_list, name="asset_list"),                 # /assets/
    path("add/", views.add_asset, name="add_asset"),               # /assets/add/
    path("<int:pk>/", views.asset_detail, name="asset_detail"),    # /assets/1/
    path("<int:pk>/edit/", views.edit_asset, name="edit_asset"),   # /assets/1/edit/
    path("<int:pk>/delete/", views.delete_asset, name="delete_asset"), # /assets/1/delete/

    # Reservations (note -> full path is /assets/reservation/...)
    path("reservation/", views.reservation_list, name="reservation_list"),
    path("reservation/add/", views.add_reservation, name="add_reservation"),
    path("reservation/<int:pk>/checkout/", views.checkout_reservation, name="checkout_reservation"),
]
