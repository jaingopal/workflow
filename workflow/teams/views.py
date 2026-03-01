from django.shortcuts import render,redirect,HttpResponse
from users.models import User
from .models import Team


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
        del request.session['count']
        del request.session['teamid']
        del request.session['name']
        
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