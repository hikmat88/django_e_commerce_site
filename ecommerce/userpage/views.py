from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.contrib import messages
from .forms import *

# Create your views here.


def homepage(request):
    products = Product.objects.all().order_by("-id")[:8]
    context = {"products": products}
    return render(request, "userpage/home.html", context)


def productdetails(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, "userpage/productdetails.html", context)


def show_product(request):
    product = Product.objects.all()
    context = {"products": product}
    return render(request, "userpage/product.html", context)


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    check_item_presence = Cart.objects.filter(user=user, product=product)
    if check_item_presence:
        messages.add_message(request, messages.ERROR, "product alredy in the cart")
        return redirect("/products")
    else:
        cart = Cart.objects.create(product=product, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, "product added to cart")
            return redirect("/cart")
        else:
            messages.add_message(request, messages.ERROR, "someting went wrong")
            return redirect("/product")


@login_required
def show_cart_items(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    context = {"cart": cart}
    return render(request, "userpage/cart.html", context)


@login_required
def delete_cart_item(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    messages.add_message(request, messages.SUCCESS, "cart items is delete")
    return redirect("/cart")


@login_required
def order_item(request, product_id, cart_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(id=cart_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get("quantity")
            price = product.Product_price
            total_price = int(quantity) * int(price)
            phone_no = request.POST.get("phone_no")
            address = request.POST.get("address")
            payment_method = request.POST.get("payment_method")
            payment_status = request.POST.get("payment_status")

            order = Order.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                phone_no=phone_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status,
            )
            if order.payment_method == "Cash on Delivery":
                cart = Cart.objects.get(id=cart_id)
                cart.delete()
                messages.add_message(request, messages.SUCCESS, "order completed")
                return redirect("/myorder")
            elif order.payment_method == "Esewa":
                context = {
                    "order": order,
                    "cart": cart_item,
                }
                return render(request, "userpage/esewa_payment.html", context)
            else:
                messages.add_message(request, messages.ERROR, "something went wrong")
                return render(request, "userpage/orderform.html", {"forms": order})
    context = {"forms": OrderForm}
    return render(request, "userpage/orderform.html", context)


@login_required
def my_order(request):
    user = request.user
    order = Order.objects.filter(user=user)

    context = {"items": order}
    return render(request, "userpage/myorder.html", context)


import requests as req


def esewa_verify(request):
    import xml.etree.ElementTree as ET

    o_id = request.GET.get("o_id")
    amount = request.GET.get("amt")
    refId = request.GET.get("refId")
    url = "https://uat.esewa.com.np/epay/main"
    d = {"amt": amount, "scd": "EPAYMENT", "rid": refId, "pid": o_id}
    resp = req.post(url, id)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == "Success":
        order_id = o_id.split("_")[0]
        order = Order.objects.get(id=order_id)
        order.payment_status = True
        order.save()
        cart_id = o_id.split("_")[1]
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request, messages.SUCCESS, "order sucessfull")
        return redirect("/order")
    else:
        messages.add_message(request, messages.ERROR, "failed to complete order")
        return redirect("/cart")
