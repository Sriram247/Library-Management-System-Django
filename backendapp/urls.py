from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.list_tables, name='list_tables'),
    path('add-book/', views.add_book, name='add_book'),
    path('<str:table_name>/', views.view_table, name='view_table'),
    path('<str:table_name>/add/', views.add_edit_row, name='add_row'),
    path('<str:table_name>/<int:row_id>/edit/', views.add_edit_row, name='edit_row'),
    path('<str:table_name>/<int:row_id>/delete/', views.delete_row, name='delete_row'),

]
