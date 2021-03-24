from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('favorite/<int:q_id>', views.favorite),
    path('unfavorite/<int:q_id>', views.unfavorite),
    path('delete_quote/<int:q_id>', views.delete_quote),
    path('login', views.login),
    path('logout', views.logout),
    path('post_quote', views.post_quote),
    path('quotes', views.quotes),
    path('register', views.register),
    path('user', views.quotes),
    path('user/<int:id>', views.user),
    path('myaccount/<int:id>', views.myaccount),
    path('myaccount/edit/<int:id>', views.myaccount_edit),
]