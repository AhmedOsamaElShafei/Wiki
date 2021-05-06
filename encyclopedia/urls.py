from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("NewPage",views.CreateNewPage, name="newPage"),
    path("edit/<str:entry>", views.edit, name="editPage")
]
