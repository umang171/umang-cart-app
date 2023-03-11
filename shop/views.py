from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
import math
import json


def index(request):
    products = Product.objects.all()

    all_prods = []
    catprods = Product.objects.values("category")
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        no_of_slides = n//4+math.ceil(n/4-n//4)
        all_prods.append([prod, no_of_slides, range(1, no_of_slides)])
    params = {
        "all_prods": all_prods
    }
    # print(products, n, no_of_slides, range(1, no_of_slides))
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        desc = request.POST.get("desc", "")
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop/contact.html")


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get("orderid")
        email = request.POST.get("email")
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append(
                        {"text": item.update_desc, "time": item.timestamp})
                response_update = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response_update)
            else:
                return HttpResponse("{}")                
        except:
            return HttpResponse("{}")

    return render(request, "shop/tracker.html")


def search(request):
    return render(request, "shop/search.html")


def product_view(request, myid):
    product = Product.objects.filter(id=myid)
    params = {"product": product[0]}
    return render(request, "shop/product_view.html", params)


def checkout(request):
    if request.method == "POST":
        itemJson = request.POST.get("itemJson", "")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")
        phone = request.POST.get("phone", "")
        print(itemJson)
        order = Orders(items_json=itemJson, name=name, email=email, address=address,
                       city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id
        order_update = OrderUpdate(
            order_id=order.order_id, update_desc="Your order has been placed")
        order_update.save()
        return render(request, "shop/checkout.html", {'thank': thank, "id": id})
    return render(request, "shop/checkout.html")
