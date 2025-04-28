from django.urls import path
from .views import TaskListView, RandomTaskView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/random/', RandomTaskView.as_view(), name='random-task'),
]
