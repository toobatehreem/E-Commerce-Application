from ast import Or
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from .models import Product, Product_Type
from django.views import View
from django.core.files.storage import FileSystemStorage
from .models import Product, Order, Order_Item
# Create your views here.
class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity +1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart

        print(request.session['cart'])
        return redirect("/")

    def get(self, request):
        if request.user.is_authenticated:
            pass
        else:
            if request.session.get('cart'):
                request.session.get('cart').clear()
        products = Product.objects.all()
        return render(request, 'App/index.html', context={'products':products, 'paths':'../../media'})
# def index(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         if request.session.get('cart'):
#             request.session.get('cart').clear()
#     return render(request, 'App/index.html')

def categories(request):
    categories=[]
    product_categories = Product_Type.choices
    for i in range(len(product_categories)):
        categories.append(product_categories[i][1])
    context = {'product_categories': categories}
    return render(request, 'App/categories.html', context=context)

class Kurti_Index(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity +1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart

        print(request.session['cart'])
        return redirect("/categories/Kurti")

    def get(self, request):
        if request.user.is_authenticated:
            pass
        else:
            if request.session.get('cart'):
                request.session.get('cart').clear()
        kurtis = None
        kurtis = Product.objects.filter(product_type='Kurti')
        context = kurtis
        return render(request, 'App/kurti.html', context={'kurtis':context, 'paths':'../../media'})

class Trousers_Index(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity +1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect("/categories/Trousers")

    def get(self, request):
        if request.user.is_authenticated:
            pass
        else:
            if request.session.get('cart'):
                request.session.get('cart').clear()
        trousers = None
        trousers = Product.objects.filter(product_type='Trousers')
        context = trousers
        return render(request, 'App/trousers.html', context={'trousers':context, 'paths':'../../media'})

class Cart(View):   
    def get(self , request):
        if request.session.get('cart'):
            ids = list(request.session.get('cart').keys())
            products = Product.get_products_by_id(ids)
            return render(request , 'App/cart.html' , context={'products' : products, 'paths':'../../media'} )
        else:
            return render(request , 'App/cart.html')

class CheckOut(View):
    def get(self, request):
        return render(request, 'App/checkout.html')

    def post(self, request):
        # address = request.POST.get('address')
        # phone = request.POST.get('phone')
        print("here")
        customer = request.user
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(products)
        print(customer, cart, products)

        for product in products:
            print(cart.get(str(product.product_id)))
            order = Order(user_id = customer)
            order.save()
            order_id = order
            print(order_id)
            product_id = product
            print(product_id)
            quantity=cart.get(str(product.product_id))
            order_item = Order_Item(order_id = order_id, product_id = product_id, quantity=quantity)
            order_item.save()
            #     customer=Customer(id=customer),
            #               product=product,
            #               price=product.price,
            #               address=address,
            #               phone=phone,
            #               quantity=cart.get(str(product.id)))
            # order.save()
        request.session['cart'] = {}

        return redirect('App:checkout')


def add_products(request):
    if request.method == "POST" and request.FILES['image']:
        name = request.POST.get('name')
        image = request.FILES['image']
        fss = FileSystemStorage()
        fss.save(image.name, image)
        types = request.POST.get('types')
        price = request.POST.get('price')
        products = Product(product_name=name,  product_image=image, product_type=types, price=price)
        products.save()
        messages.success(request, "Product added successfully!")
        return redirect('App:add_products')
    else:
        return render(request, 'App/add_products.html')

def see_orders(request):
    orders = Order.objects.filter(completed=False)
    order_items = Order_Item.objects.all()
    return render(request, 'App/see_orders.html', context={'orders':orders, 'order_items':order_items})

def loginuser(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("App:index")
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Invalid credentials")

    form = AuthenticationForm()
    return render(request=request, template_name='App/login.html', context={'login_form':form})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print(request.POST.get('username'))
        print(request.POST.get('email'))
        print(request.POST.get('password1'))
        print(request.POST.get('address'))
        print(request.POST.get('phone'))
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("App:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        print("Something failed")
    form = NewUserForm()
    return render(request=request, template_name="App/register.html", context={'register_form':form})

def logoutuser(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect("App:index")