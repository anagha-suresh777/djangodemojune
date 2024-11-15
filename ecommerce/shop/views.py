from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from shop.models import Category,Product
# Create your views here.
def categories(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'categories.html',context)

def products(request,p):
    k = Category.objects.get(id=p)  # reads a particular record
    p=Product.objects.filter(category=k)
    context = {'particular': k,'product':p}
    return render(request, 'products.html',context)




def details(request,p):
    pro=Product.objects.get(id=p)
    context={'productdetail':pro}
    return render(request, 'productdetails.html',context)


def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        pa = request.POST['pa']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e=request.FILES.get('e')
        if(pa==cp):
            u=User.objects.create_user(username=u,password=pa,email=e,first_name=f,last_name=l)
            u.save()
            return redirect('shop:categories')
        else:
            return HttpResponse("Passwords are not same")

    return render(request, 'register.html')

def user_login(request):
    if(request.method=="POST"):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:categories')
        else:#if no matching user
            return HttpResponse("Invalid Credentials")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('shop:login')


def addcategories(request):
    if (request.method == "POST"):
        n=request.POST['n']
        i=request.FILES['i']
        d = request.POST['d']
        c = Category.objects.create(name=n,image=i,description=d)
        c.save()
        return redirect('shop:categories')
    return render(request,'addcategory.html')

def addproduct(request):
    if (request.method == "POST"):
        n=request.POST['n']
        i=request.FILES['i']
        d = request.POST['d']
        s = request.POST['s']
        p = request.POST['p']
        c = request.POST['c']
        cat=Category.objects.get(name=c)
        p = Product.objects.create(name=n,image=i,desc=d,stock=s,price=p,category=cat)
        p.save()
        return redirect('shop:categories')
    return render(request,'addproduct.html')


def addstock(request,i):
    product=Product.objects.get(id=i)

    if(request.method=="POST"):  #After form submission
        product.stock=request.POST['s']
        product.save()
        return redirect('shop:details',i)

    context={'pro':product}
    return render(request, 'addstock.html',context)