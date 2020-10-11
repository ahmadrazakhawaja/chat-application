from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create", views.create, name="create"),
    path("listing/<id>", views.listingc, name="listing"),
    path("watchlist", views.watchlistk, name="watchlist"),
    path("category", views.categoryl, name="category"),
    path("category/<category>", views.categorylx, name="categoryx")


]
