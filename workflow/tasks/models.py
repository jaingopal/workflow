from django.db import models

# Create your models here.
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    ALLOWED_STATES = [("TODO",'To do'),("IN_PROGRESS",'In progress'),("DONE",'Done')]
    IMPORTANCE_STATES = [('LOW','Low'),('MEDIUM','Medium'),('HIGH','High')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    team = models.ForeignKey("teams.Team",on_delete=models.CASCADE,related_name="tasks")
    assigned = models.ForeignKey("users.User",on_delete=models.SET_NULL,null=True,blank=True)
    progress = models.CharField(max_length = 20,choices=ALLOWED_STATES,default='TODO')
    importance = models.CharField(max_length=20,choices=IMPORTANCE_STATES,default='LOW')
    deadline = models.DateField()
    time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title