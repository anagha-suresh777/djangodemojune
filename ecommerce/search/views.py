from django.shortcuts import render
from shop.models import Category,Product
from django.db.models import Q
# Create your views here.
def search_products(request):
    if(request.method=="POST"):
        query=request.POST['q']
        if query:
            result=Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
            context={'res':result,'query':query}
    return render(request,'search.html',context)