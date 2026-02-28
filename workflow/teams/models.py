from django.db import models


# Create your models here.
class Team(models.Model):
    team_leader = models.ForeignKey("users.User",on_delete=models.CASCADE)
    team_members= models.ManyToManyField("users.User",related_name="teams")
    team_id = models.SlugField()
    
    def __str__ (self):
        return self.team_id
    