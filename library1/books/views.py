from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):#home view
    return render(request, 'home.html')

from books.models import Book
@login_required
def viewbooks(request):#index view

    k=Book.objects.all()  #reads all records from tge book table
    context={'book':k}    #sends data from view function to html page
    return render(request,'view.html',context)
@login_required
def addbooks(request):#index view
    if(request.method=="POST"):
        t=request.POST['t']
        a = request.POST['a']
        p = request.POST['p']
        pa = request.POST['pa']
        l = request.POST['l']
        i=request.FILES.get('i')
        f=request.FILES.get('f')
        b=Book.objects.create(title=t,author=a,price=p,pages=pa,language=l,cover=i,pdf=f)
        b.save()
        return viewbooks(request)
    return render(request, 'add.html')

@login_required
def detail(request,p):
    k=Book.objects.get(id=p) #reads a particular record
    context={'particular':k}
    return render(request, 'detail.html',context)

@login_required
def delete(request,p):
    k=Book.objects.get(id=p)
    k.delete()
    return redirect('books:view')
@login_required
def edit(request,p):
    k = Book.objects.get(id=p)
    if (request.method == "POST"):
        k.title = request.POST['t']
        k.author= request.POST['a']
        k.price= request.POST['p']
        k.pages= request.POST['pa']
        k.language = request.POST['l']
        if(request.FILES.get('i')==None):
            k.save()
        else:
            k.cover=request.FILES.get('i')

        if(request.FILES.get('f')==None):
            k.save()
        else:
            k.pdf=request.FILES.get('f')

        k.save()
        return redirect('books:view')

    context={'edit':k}
    return render(request, 'edit.html',context)
