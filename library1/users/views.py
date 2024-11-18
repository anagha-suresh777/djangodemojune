from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from users.models import CustomUser
from users.models import Users
# Create your views here.
def userregister(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e=request.FILES.get('e')
        n=request.POST['n']
        a=request.POST['a']
        if(p==cp):
            u=CustomUser.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l,phone=n,address=a,is_user=True)
            u.save()
            return redirect('books:home')
        else:
            return HttpResponse("Passwords are not same")


    return render(request, 'userregister.html')

def adminregister(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e=request.FILES.get('e')
        n=request.POST['n']
        a=request.POST['a']
        if(p==cp):
            u=CustomUser.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l,phone=n,address=a,is_superuser=True)
            u.save()
            return redirect('books:home')
        else:
            return HttpResponse("Passwords are not same")


    return render(request, 'adminregister.html')

def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user and user.is_superuser==True:
            login(request,user)
            return redirect('books:home')
        elif user and user.is_user==True:
            login(request, user)
            return redirect('books:home')
        else:#if no matching user
            return HttpResponse("Invalid Credentials")

    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login')



def view_user(request):
    g = CustomUser.objects.all()
    context = {'using': g}
    return render(request, 'viewusers.html',context)



