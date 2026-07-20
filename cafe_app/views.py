from django.shortcuts import render
from django.http import HttpResponse
from . models import *
from django.shortcuts import render, redirect
def home(request):
    customers = Customer.objects.all()
    categories = Category.objects.filter(status=True)
    menus = Menu.objects.filter(available=True)
    context = { "data": customers,"categories": categories,"menus": menus,}
    return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        Customer.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )
        return redirect('home')

    return render(request, 'register.html') 
def delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('home')

def update(request, id):
    customer = Customer.objects.get(id=id)

    if request.method == "POST":
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.username = request.POST.get('username')
        customer.email = request.POST.get('email')
        customer.save()

        return redirect('home')

    return render(request, 'update.html', {'datas': customer})  
        

def category_filter(request, id):
    customers = Customer.objects.all()
    categories = Category.objects.filter(status=True)
    menus = Menu.objects.filter(category_id=id, available=True)

    context = {
        "data": customers,
        "categories": categories,
        "menus": menus,
    }

    return render(request, "home.html", context)


def contact(request):

    if request.method == "POST":

        Contact.objects.create(

            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")

        )

        return redirect("home")

    return redirect("home")    

def add_to_cart(request, id):

    customer = Customer.objects.first()

    if not customer:
        return HttpResponse("No customer found in database")

    cart, created = Cart.objects.get_or_create(customer=customer)

    menu = Menu.objects.get(id=id)

    item, created = CartItem.objects.get_or_create(cart=cart,menu=menu)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')

def cart(request):

    customer = Customer.objects.first()

    if not customer:
        return HttpResponse("No customer found in database")

    cart = Cart.objects.filter(customer=customer).first()

    items = []
    total = 0

    if cart:
        items = CartItem.objects.filter(cart=cart)

        for item in items:
            total += item.total_price()

    return render(
        request,'cart.html',
        {
            'items': items,
            'total': total
        }
    
    )    

def increase_quantity(request, id):
    item = CartItem.objects.get(id=id)
    item.quantity += 1
    item.save()

    return redirect('cart')


def decrease_quantity(request, id):
    item = CartItem.objects.get(id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')    

def remove_item(request, id):
    item = CartItem.objects.get(id=id)
    item.delete()

    return redirect('cart')
def checkout(request):

    customer = Customer.objects.first()

    if not customer:
        return HttpResponse("No customer found")

    cart = Cart.objects.filter(customer=customer).first()

    if not cart:
        return HttpResponse("Cart is empty")

    items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in items:
        total += item.total_price()

    if request.method == "POST":

        order = Order.objects.create(
            customer=customer,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            total_amount=total
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                menu=item.menu,
                quantity=item.quantity,
                price=item.menu.price
            )

        items.delete()

        return redirect('order_success')

    return render(
        request,
        'checkout.html',
        {
            'items': items,
            'total': total
        }
    )
def order_success(request):
    return render(request, 'order_success.html')
def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        customer = Customer.objects.filter(
            email=email,
            password=password
        ).first()

        if customer:
            request.session['customer_id'] = customer.id
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid Email or Password'}
        )

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')    
