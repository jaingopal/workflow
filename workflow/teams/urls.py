from django.urls import path ,include
from . import views 

app_name = "teams"

urlpatterns = [
    path('',views.teampage,name = 'teampage'),
    path('register/',views.register, name = 'register'),
    path('registration/',views.add_members,name = 'add_members'),
    path('add-task/',views.add_task,name = 'add_task'),
    path('add-member/',views.add_member,name = 'add_member'),
    path('task/',include('tasks.urls')),
]
