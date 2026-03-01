from django.shortcuts import render,redirect,HttpResponse
from .models import Task
from teams.models import Team
from users.models import User
# Create your views here.

def tasks_list(request):
    if(request.session.get('user')):
        if(request.session.get('team')):
            if(request.session.get('task')):
                task = Task.objects.get(task_id = request.session.get("task"))
                teamId = request.session["team"]
                if(request.method == "POST"):
                    if(request.POST.get('nav')):
                        if(request.POST.get('nav')=='back'):
                            del request.session['task']
                            return redirect('teams:teampage')
                        if request.POST.get('nav')=='logout':
                            del request.session['task']
                            del request.session['team']
                            del request.session['user']
                            return redirect('/')
                        
                    if(request.POST.get("deadline")):
                        task.deadline = request.POST["deadline"]
                        task.save()
                        return render(request,'task.html',{"task":task})
                    if(request.POST.get("importance")):
                        task.assigned = request.POST["importance"]
                        task.save()
                        return render(request,'task.html',{"task":task})
                    if(request.POST.get("new_member")):
                        userid = request.POST["new_member"]
                        if(User.objects.get(userid = userid) in Team.objects.get(team_id = teamId).team_members.all()):
                            task.assigned = User.objects.get(userid = userid)
                            task.save()
                            return render(request,"task.html",{"task":task})
                        return render(request,"task.html",{"task":task,"error":"Userid is invalid"})
                    if(request.POST.get("member_name")):
                        userid = request.POST.get("member_name")
                        if(User.objects.get(userid = userid) in Team.objects.get(team_id = teamId).team_members.all()):
                            task.assigned = User.objects.get(userid = userid)
                            task.save()
                            return render(request,"task.html",{"task":task})
                        return render(request,"task.html",{"task":task,"error":"Userid is invalid"})
                    if(request.POST.get('action')=='remove_member'):
                        task.assigned = None
                        task.save()
                        return render(request,"task.html",{"task":task})
                    if(request.POST.get('action')=='delete'):
                        del request.session['task']
                        task.delete()
                        return redirect('teams:teampage')
                return render(request,"task.html",{"task":task})
            else:
                return redirect('teams:teampage')
        else:
            return redirect('/')
    else:
        return redirect('/')
    