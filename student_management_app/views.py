from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


from student_management_app.EmailBackEnd import EmailBackEnd


def showDemoPage(request):
   return  render(request,"demo.html")


def showLoginPage(request):
   return  render(request,"login_page.html")

def doLogin(request):
   if request.method!="POST":
      return HttpResponse("<h2>Method not allowd</h2>")
   else:
      user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
      if user!=None:
               login(request,user)
               return HttpResponseRedirect("/admin_home")
               # return HttpResponse("Email :" +request.POST.get("email")+" Password : "+request.POST.get("password"))
      else:
           messages.error(request,"Invalid Login Detials")
           return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user !=None:
       return HttpResponse("User:"+request.user.email+" usertype:"+request.user.user_type)
    else:
       return HttpResponse("Pls Login First")


def logout_user(request):
   logout(request)
   return HttpResponseRedirect("/")
