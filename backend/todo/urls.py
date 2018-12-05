from django.urls import include, path
from . import views


urlpatterns = [
    path('todo/', views.todo_list, name='todo'),
    path('todo/<int:id>/', views.target_todo, name='target_todo'),
]