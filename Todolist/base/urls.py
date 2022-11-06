from django.urls import path
from . import views
from . views import Tasklist,TaskDeatil,CreateTask,UpdateTask,DeleteTask,CustomLoginView,UserRegisterView
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path('login/',UserRegisterView.as_view(), name = 'register'),
    path('register/',CustomLoginView.as_view(), name = 'login'),
    path('logout/',LogoutView.as_view(next_page='login'), name = 'logout'),
    path('',Tasklist.as_view(), name = 'task_list'),
    path('tasks/<int:pk>',TaskDeatil.as_view(), name = 'tasks'),
    path('create-task/',CreateTask.as_view(), name = 'create_task'),
    path('tasks-update/<int:pk>',UpdateTask.as_view(), name = 'tasks_update'),
    path('tasks-delete/<int:pk>',DeleteTask.as_view(), name = 'tasks_delete'),

]
