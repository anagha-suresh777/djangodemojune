from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart,Payment,Order_details
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay
# Create your views here.
@login_required
def add_to_cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
       c=Cart.objects.get(product=p,user=u)
       if(p.stock>0):
           c.quantity+=1
           c.save()
           p.stock-=1
           p.save()
    except:
        if(p.stock>0):
            c = Cart.objects.create(product=p, user=u, quantity=1)
            c.save()
            p.stock-=1
            p.save()
    return redirect('cart:cartview')

@login_required
def cart_view(request):
    u=request.user


    c = Cart.objects.filter(user=u)
    total = 0
    total2=0
    for i in c:
        total+=i.quantity*i.product.price
        total2+=total+45



    context={'cart':c,'total':total,'totalprice':total2}

    return render(request,'cart.html',context)

@login_required
def cart_remove(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        c = Cart.objects.get(product=p, user=u)
        if (c.quantity > 1):
            c.quantity -= 1
            c.save()
            p.stock += 1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass

    return redirect('cart:cartview')

@login_required
def cart_delete(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(product=p, user=u)
        c.delete()
        p.stock+=c.quantity
        p.save()

    except:
        pass

    return redirect('cart:cartview')

def billing(request):
    if(request.method=="POST"):
        address=request.POST['a']
        phone=request.POST['p']
        pin=request.POST['pi']
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        total2=0
        for i in c:
            total+=i.quantity*i.product.price
            total2+= total + 45
        total1=int(total2*100)
        client=razorpay.Client(auth=('rzp_test_MZ9PRMd3HXxubh','LlS4Cb9MwYrX6URGobkW55fy')) #creates a client connection
        response_payment=client.order.create(dict(amount=total1,currency="INR")) #creates an order with razorpay using razorpay client
        print(response_payment)
        order_id=response_payment['id']
        status=response_payment['status']


        if(status=="created"):
            p=Payment.objects.create(name=u.username,amount=total2,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(prod=i.product,use=u,no_of_items=i.quantity,address=address,phone_no=phone,pin=pin,order_id=order_id)
                o.save()
        response_payment['name']=u.username
        context={'payment':response_payment}
        return render(request,'payment.html',context)

    return render(request, 'checkout.html')

@csrf_exempt
def payment_status(request,u):
    usr = User.objects.get(username=u)
    if not request.user.is_authenticated:
        login(request,usr)


    if(request.method=="POST"):
        response=request.POST
        print(response)

        param_dict={
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        client = razorpay.Client(auth=('rzp_test_MZ9PRMd3HXxubh', 'LlS4Cb9MwYrX6URGobkW55fy'))
        try:
                status=client.utility.verify_payment_signature(param_dict)
                print(status)

              #to retrieve a particular record from payment table matching with razorpay response order id
                p=Payment.objects.get(order_id=response['razorpay_order_id'])
                p.razorpay_payment_id=response['razorpay_payment_id']
                p.paid=True
                p.save()

                #to retrieve a records from Order_details table matching with razorpay response order id
                o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
                for i in o:
                    i.payment_status="completed"
                    i.save()


                c=Cart.objects.filter(user=usr)
                c.delete()
        except:
            pass

    return render(request,'payment_status.html',{'status':status})



@login_required
def order_view(request):
    u=request.user
    o=Order_details.objects.filter(use=u)
    context={'orders':o}
    return render(request,'order_view.html',context)