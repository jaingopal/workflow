from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Team(models.Model):
    team_leader = models.ForeignKey("users.User",on_delete=models.CASCADE)
    team_members= models.ManyToManyField("users.User",related_name="teams")
    team_id = models.SlugField(unique=True)
    team_name = models.CharField(max_length=75, default="")
    
    def __str__ (self):
        return self.team_id
    
    @classmethod
    def valid (cls,data):
        id = Team._meta.get_field("team_id")
        try : 
            id.clean(data,None)
            return True 
        
        except ValidationError:
            return False
        
        