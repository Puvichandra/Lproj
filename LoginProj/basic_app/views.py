from django.shortcuts import render
from django.conf.urls import  url
from basic_app.form  import Userform, pfform

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered =False

    if request.method=='POST':
        u_form = Userform(data=request.POST)
        p_form = pfform(data=request.POST)

        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user.set_password(user.password)
            user.save()

            profile=p_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
                profile.save()
                registered=True
            else:
                print(u_form.errors, p_form.errors)


    else:
        u_form=Userform()
        p_form=pfform()

    return render(request,'basic_app/registration.html', {'Userform': Userform,
                                                         'pfform':pfform,
                                                         'registered': registered})


def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active")
        else:
            print("Someone tried to login and failed")
            print("User name: {} Password:{}".format(username,password))
            return HttpResponse("Invalid credentials")
    else:
        return render(request,'basic_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("You are logged in! Nice")
