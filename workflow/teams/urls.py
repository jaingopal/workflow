from django.urls import path 
from . import views 

app_name = "teams"

urlpatterns = [
    path('register/',views.register, name = 'register'),
    path('registration/',views.add_members,name = 'add_members')
]
