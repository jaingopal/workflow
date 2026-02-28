from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    name = models.CharField()
    userid = models.SlugField(unique=True)
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return self.userid
    
    def set_password(self,raw_password):
        self.password=make_password(raw_password)
        
    def check_password(self,raw_password):
        return check_password(raw_password,self.password)