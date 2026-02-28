from django.shortcuts import render,redirect,HttpResponse
from users.models import User
from .models import Team


def add_members(request):
    if(request.method == "POST"):
        leader = request.session["leader"]
        count = int(request.session["count"])
        teamid = request.session["teamid"]
        team = Team()
        team.team_leader=User.objects.get(userid = leader)
        team.team_id=teamid
        for i in range(1,count):
            member_id= request.POST.get(f'member{i}')
            if(member_id == leader):
                return render(request,"add-team-members.html",{"error":f"Member {i} is Leader which is not feasible","leader":leader,"count":range(1,count)})
            try : 
                User.objects.get(userid=member_id)
                
            except User.DoesNotExist:
                return render(request,"add-team-members.html",{"error":f"UserId of Member {i} is wrong","leader":leader,"count":range(1,count)})
            
        team.save()
        for i in range(1,count):
            member_id=request.POST.get(f'member{i}')
            team.team_members.add(User.objects.get(userid=member_id))
            
        return HttpResponse("Test for registering team")
    
    count = int(request.session["count"])
    leader = request.session["leader"]
    return render(request,'add-team-members.html',{"leader":leader,"count":range(1,count)})
        

def register(request):
    if(request.method == "POST"):
        
        userid = request.POST.get("userid")
        
        try : 
            user = User.objects.get(userid=userid)
            password = request.POST.get("password")
            if(not(user.check_password(password))):
                return render(request,"register-team.html",{"error":"Password not matched"})
            count = (request.POST.get("count"))
            teamid = (request.POST.get("teamid"))
            if(Team.valid(teamid)):
                try :
                    Team.objects.get(team_id = teamid)
                    return render(request,"register-team.html",{"error":"TeamId already exists"})
                except Team.DoesNotExist:
                    pass
            else:
                return render(request,"register-team.html",{"error":"TeamId is not valid"})
            
            request.session['leader'] = userid
            request.session['count'] = count
            request.session['teamid'] = teamid

            return redirect('teams:add_members')
            
        except User.DoesNotExist:
            return render(request,"register-team.html",{"error":"Wrong UserName or Leader not registered"})
           
    return render(request,"register-team.html")