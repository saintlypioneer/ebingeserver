from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Client, Product, Order, OrderedProducts
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
# Create your views here.

def homepage(request):
    template = loader.get_template('home.html')
    context = {'title': 'Home'}
    return HttpResponse(template.render(request, context))
def shop(request):
    template = loader.get_template('shop.html')
    context = {}
    return HttpResponse(template.render(request, context))

@csrf_exempt
def detail(request, pid):
    if request.method == 'GET':
        product = Product.objects.all().filter(uid=pid)[0]
        template = loader.get_template('detail.html')
        context = {'product': product}
        return HttpResponse(template.render(context, request))

@csrf_exempt
def productJsonDetail(request):
    if request.method == 'POST':
        pids = json.loads(request.body)['pids']
        returnJson = {}
        for i in range(len(pids)):
            product = Product.objects.all().filter(uid=pids[i])[0]
            returnJson.update({i: {'pk':product.uid, 'image': product.image.url, 'name': product.name, 'cost_price': product.cost_price, 'discount_price': product.selling_price - product.cost_price}})
        return JsonResponse(returnJson, safe=False)
def cart(request):
    template = loader.get_template('cart.html')
    context = {'title':'Title'}
    return HttpResponse(template.render(request, context))
def checkout(request):
    if request.method == 'GET':
        template = loader.get_template('checkout.html')
        context = {'title': 'Checkout'}
        return HttpResponse(template.render(request, context))
    elif request.method == 'POST':
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        email = request.POST['email']
        pno = request.POST['phone']
        add1 = request.POST['address1']
        add2 = request.POST['address2']
        state = request.POST['state']
        cart = request.POST['hiddenCart']
        temp = Client.objects.get(detail = User.objects.get(email = request.user.email))
        temp.add1 = add1
        temp.add2 = add2
        temp.state = state
        temp.cart = cart
        temp.save()
        cartJson = json.loads(cart)
        if len(cartJson)<1 :
            messages.info(request, 'Please add elements to cart first !')
            return redirect("/shop")
        else :
            tempOrder = Order(
                client = temp,
                fname = fname,
                lname = lname,
                mob = pno,
                add1 = add1,
                add2 = add2,
                state = state
            )
            tempOrder.save()
            for key in cartJson.keys():
                product = Product.objects.all().filter(uid = key)[0]
                OrderedProducts(
                    selling_price = product.selling_price,
                    order = tempOrder,
                    product = product
                ).save()
            messages.info(request, 'Order Created ! Please be patient. You will receive it within 24 Hrs.')
            return redirect("/")
def login(request):
    if request.method == 'GET':
        template = loader.get_template('login.html')
        context = {'title': 'Login'}
        return HttpResponse(template.render(request, context))
    elif request.method == 'POST':
        uemail = request.POST['inputEmail']
        psd = request.POST['inputPassword']
        usr = auth.authenticate(username=uemail.split("@")[0], password=psd)
        if usr is not None:
            auth.login(request, usr)
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect("login")
def signup(request):
    if request.method == 'GET':
        template = loader.get_template('signup.html')
        context = {'title': 'Signup'}
        return HttpResponse(template.render(request, context))
    elif request.method == 'POST':
        fname = request.POST['inputName']
        lname = request.POST['inputName2']
        email = request.POST['inputEmail1']
        mob = request.POST['inputNumber']
        psd = request.POST['inputPassword1']
        cpsd = request.POST['inputPassword2']
        if psd != cpsd:
            messages.info(request, "Password and Confirm Password don't match")
            return redirect("signup")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "User with this email already exists! Please Login")
            return redirect("login")
        else:
            usr = User.objects.create_user(
                first_name = fname,
                last_name = lname,
                email = email,
                password = psd,
                username = email.split("@")[0]
            )
            usr.save()
            cli = Client(
                detail = usr,
                mob = mob
            )
            cli.save()
            messages.info(request, "User Created! Please Signup.")
            return redirect("login")
def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out")
    return redirect("/")

@csrf_exempt
def shoppagedata(request):
    data = json.loads(request.body)
    category = data['category']
    sub_category = data['sub_category']
    if (category == ''):
        products = Product.objects.all().filter(category__isnull=False, sub_category=sub_category)
    elif (sub_category == ''):
        products = Product.objects.all().filter(category=category, sub_category__isnull=False)
    elif (sub_category == '' and category == ''):
        products = Product.objects.all().filter(category__isnull=False, sub_category__isnull=False)
    else:
        products = Product.objects.all().filter(category=category, sub_category=sub_category)
    return JsonResponse(serializers.serialize('json', products), safe=False)

def profile(request):
    template = loader.get_template('profile.html')
    context = {'title': 'Profile'}
    return HttpResponse(template.render(request, context))
