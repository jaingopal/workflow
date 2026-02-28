from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

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
    
    @classmethod
    def is_valid_user (value):
        id = User._meta.get_field("userid")
        passw = User._meta.get_field("password")
        name_t = User._meta.get_field("name")
        
        try : 
            id.clean(value["userid"],None)
            passw.clean(value["password"],None)
            name_t.clean(value["name"],None)
            return True 
        except ValidationError:
            return False
        