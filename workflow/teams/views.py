from django.shortcuts import render,redirect,HttpResponse
from users.models import User
from .models import Team
from tasks.models import Task

def add_members(request):
    if(not(request.session.get('user'))):
        return render(request,"not-logged-in.html")
    
    if(not(request.session.get('count') and request.session.get('teamid') and request.session.get('name'))):
        return redirect('teams:register')
    
    if(request.method == "POST"):
        leader = request.session["user"]
        count = int(request.session["count"])
        teamid = request.session["teamid"]
        name = request.session["name"]
        team = Team()
        team.team_leader=User.objects.get(userid = leader)
        team.team_id=teamid
        team.team_name = name
        
        for i in range(1,count):
            member_id= request.POST.get(f'member{i}')
            if(member_id == leader):
                return render(request,"add-team-members.html",{"error":f"Member {i} is Leader which is not feasible","leader":leader,"count":range(1,count)})
            try : 
                User.objects.get(userid=member_id)
                
            except User.DoesNotExist:
                return render(request,"add-team-members.html",{"error":f"UserId of Member {i} is wrong","leader":leader,"count":range(1,count)})
        team.save()
        team.team_members.add(User.objects.get(userid=leader))
        for i in range(1,count):
            member_id=request.POST.get(f'member{i}')
            team.team_members.add(User.objects.get(userid=member_id))
        
        del request.session['count']
        del request.session['teamid']
        del request.session['name']
            
        return redirect('/')
    
    count = int(request.session["count"])
    leader = request.session["user"]
    return render(request,'add-team-members.html',{"leader":leader,"count":range(1,count)})
        

def register(request):
    if(not(request.session.get("user"))):
        return render(request,"not-logged-in.html")
    
    if(request.method == "POST"):
        try : 
            count = (request.POST.get("count"))
            teamid = (request.POST.get("teamid"))
            name = request.POST.get("name")
            if(Team.valid(teamid)):
                try :
                    Team.objects.get(team_id = teamid)
                    return render(request,"register-team.html",{"error":"TeamId already exists"})
                except Team.DoesNotExist:
                    pass
            else:
                return render(request,"register-team.html",{"error":"TeamId is not valid"})
            
            request.session['count'] = count
            request.session['teamid'] = teamid
            request.session["name"]=name

            return redirect('teams:add_members')
            
        except User.DoesNotExist:
            return render(request,"register-team.html",{"error":"Wrong UserName or Leader not registered"})
           
    return render(request,"register-team.html")


def teampage(request):
    if(request.method == "POST"):
        if(request.POST.get("action")):
            if(request.POST["action"]=="add_task"):
                return redirect('teams:add_task')
            
            if(request.POST["action"]=="add_member"):
                return redirect('teams:add_member')
                
            if(request.POST["action"]=="back"):
                del request.session["team"]
                return redirect('/')
            del request.session["team"]
            del request.session["user"]
            return redirect('/')
        if(request.POST.get("task")):
            request.session["task"]=request.POST.get("task")
            return redirect('teams:tasks:home')
        if(request.POST.get('member')):
            userid = request.POST['member']
            teamid = request.session['team']
            team = Team.objects.get(team_id = teamid)
            team.team_members.remove(User.objects.get(userid=userid))
            team.save()
            return render(request,'team_page.html',{"team":team})
            
    if(request.session.get("team") and request.session.get("user")):
        try :
            team = Team.objects.get(team_id = request.session.get("team"))
            return render(request,"team_page.html",{"team":team})
        except Team.DoesNotExist:
            del request.session["team"]
            return redirect('/')
            
    else:
        return redirect ('/')
    
def add_task(request):
    
    if(request.method == "POST"):
        
        if(request.POST.get("action")):
            
            if(request.POST["action"]=="back"):
                return redirect('teams:teampage')
            
            del request.session["team"]
            del request.session["user"]
            return redirect('/')
        
        task = Task()
        task.title = request.POST.get("title")
        task.description=request.POST.get("description")
        if(request.POST.get("assigned")):
            try :
                user = User.objects.get(userid=request.POST.get("assigned"))
                task.assigned=user
            except User.DoesNotExist:
                return render(request,'add_task.html',{'error':"Wrong User ID"})
                
        if(request.POST.get("importance")!=""):
            task.importance=request.POST.get("importance")
        task.deadline=request.POST.get("deadline")
        task.team = Team.objects.get(team_id = request.session.get("team"))
        task.save()
        return redirect('teams:teampage')
    
    if(request.session.get("team") and request.session.get("user")):
        return render(request,'add_task.html')
    else:
        return redirect('/')
    

def add_member(request):
    if(request.method == "POST"):
        
        if(request.POST.get("action")):
            
            if(request.POST["action"]=="back"):
                return redirect('teams:teampage')
            
            del request.session["team"]
            del request.session["user"]
            return redirect('/')
        
        userid = request.POST.get('user_id')
        team = request.session.get("team")
        try :
            user = User.objects.get(userid=userid)
            if Team.objects.get(team_id = team).team_members.filter(userid=user.userid).exists():
                return render(request,'add_member.html',{'error':f'{user.name} is already a Member'})
            Team.objects.get(team_id = team).team_members.add(user)
            
        except User.DoesNotExist:
            return render(request,'add_member.html',{'error':"Wrong User ID"})
        
        return redirect('teams:teampage')
    
    if(request.session.get("team") and request.session.get("user")):
        return render(request,'add_member.html')
    else:
        return redirect('/')