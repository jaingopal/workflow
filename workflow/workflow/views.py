from django.shortcuts import render,redirect,HttpResponse
from users.models import User



def registerpage(request):
    if(request.session.get('user')):
        return redirect('/')
    if (request.method == "POST"):
        userid = request.POST.get("userid")
        
        try :
            User.objects.get(userid=userid)
            return render(request,"register.html",{"error":"User Already Exists"})
        
        except User.DoesNotExist:
            password = request.POST.get("password")
            name = request.POST.get("name")
            if(User.is_valid_user({"name":name,"password":password,"userid":userid})):
                user_new = User()
                user_new.name = name 
                user_new.userid = userid 
                user_new.set_password(password)
                user_new.save()
                request.session["user"]=user_new.userid 
                return redirect('/')
            else : 
                return render(request,"register.html",{"error":"Invalid UserName or Password or Name"})
    return render(request,"register.html")




def loginpage(request):
    if(request.session.get('user')):
        return redirect('/')
    if request.method=="POST":
        userid = request.POST.get("userid")
        password = request.POST.get("password")
        try : 
            user = User.objects.get(userid=userid)
            print ("password is ",password)
            if (user.check_password(password)):
                request.session["user"] = user.userid
                return redirect('/')
            
            else :
                return render(request,"login.html",{"error":"Invalid Password"})
            
        except User.DoesNotExist:
            return render(request,"login.html",{"error":"User Not Found"})
    return render(request,"login.html")


def homepage(request):
    if(request.method == "POST"):
        if(request.POST.get('team_id')):
            return HttpResponse(f"Test Page for {request.POST.get('team_id')}")
        del request.session["user"]
        return redirect('/')
    if(request.session.get("user")):
        userid= request.session["user"]
        user = User.objects.get(userid=userid)
        teams = user.teams.all()
        return render(request,"homepage.html",{"userid":userid,"teams":teams})
    
    return render(request,"homepage.html")