# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('addcontact', views.addcontact, name='addcontact'),
    path('contact/<str:name>/', views.contact, name='contact'),
    path('group', views.addgroup, name='group'),
    path('addgroup', views.addmember, name='addgroup'),
    path('chat/<str:name>/setting', views.setting, name='setting'),
    path('add', views.addmember, name='add'),
    path('remove', views.remove, name='remove'),
    path('admin', views.addadmin, name='admin'),
    path('radmin', views.radmin, name='radmin'),
]

