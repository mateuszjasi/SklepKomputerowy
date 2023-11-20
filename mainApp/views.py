from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Subcategory, ShopItem, Cart, Order
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
categories = Category.objects.all()


def home(response):
    return render(response, "mainApp/home.html", {"categories": categories})


def user(response):
    if response.user.is_authenticated:
        user_orders = response.user.order.all()
        user_orders = user_orders.order_by("archival", "-id")

        if response.method == "POST":
            if response.POST.get("delivered"):
                order = user_orders.get(id=response.POST.get("delivered", ""))
                order.archival = True
                order.save()
                user_orders = user_orders.order_by("archival", "-id")

        return render(response, "mainApp/user.html", {"user": response.user, "orders": user_orders, "categories": categories})

    else:
        return render(response, "mainApp/user.html", {"user": response.user, "categories": categories})


def update_cart_payment_sum(user_cart):
    payment_sum = 0
    for item in user_cart.cartitem_set.all():
        payment_sum += item.product.price * item.amount

    return payment_sum


def cart(response):
    if response.user.is_authenticated:
        user_cart = response.user.cart.first()

        if user_cart is not None:
            payment_sum = update_cart_payment_sum(user_cart)

            if response.method == "POST":
                if response.POST.get("remove"):
                    cart_item = user_cart.cartitem_set.get(id=response.POST.get("remove", ""))
                    cart_item.delete()
                    payment_sum = update_cart_payment_sum(user_cart)
                    if response.user.cart.first().cartitem_set.count() == 0:
                        user_cart.delete()
                        return HttpResponseRedirect("/cart")

                if response.POST.get("clear"):
                    user_cart.delete()
                    return HttpResponseRedirect("/cart")

            return render(response, "mainApp/cart.html", {"user_cart": user_cart, "payment_sum": payment_sum, "categories": categories})

        else:
            return render(response, "mainApp/cart.html", {"user_cart": user_cart, "categories": categories})
    else:
        return render(response, "mainApp/cart.html", {"categories": categories})


def product(response, prod_id):
    prod = ShopItem.objects.get(id=prod_id)

    if response.method == "POST":
        if response.POST.get("to-cart"):
            if response.user.cart.first() is None:
                new_user_cart = Cart(user=response.user)
                new_user_cart.save()
                response.user.cart.add(new_user_cart)

            user_cart = response.user.cart.first()
            for item in user_cart.cartitem_set.all():
                if prod == item.product:
                    item.amount += 1
                    item.save()
                    return render(response, "mainApp/product.html", {"product": prod, "categories": categories})

            user_cart.cartitem_set.create(product=prod, amount=1)

    return render(response, "mainApp/product.html", {"product": prod, "categories": categories})


def category_sorting(response, items, button_name):
    if response.method == "POST" and not response.POST.get("to-cart"):
        if response.POST.get("sort-name"):
            items = items.order_by("name")
            button_name = response.POST.get("sort-name", "")
        elif response.POST.get("sort-price-desc"):
            items = items.order_by("-price")
            button_name = response.POST.get("sort-price-desc", "")
        elif response.POST.get("sort-price-asc"):
            items = items.order_by("price")
            button_name = response.POST.get("sort-price-asc", "")

    return items, button_name


def category_add_to_cart(response):
    if response.method == "POST" and response.POST.get("to-cart"):
        prod = ShopItem.objects.get(id=response.POST.get("to-cart", ""))
        if response.user.cart.first() is None:
            new_user_cart = Cart(user=response.user)
            new_user_cart.save()
            response.user.cart.add(new_user_cart)

        user_cart = response.user.cart.first()
        for item in user_cart.cartitem_set.all():
            if prod == item.product:
                item.amount += 1
                item.save()
                return render(response, "mainApp/product.html", {"product": prod, "categories": categories})

        user_cart.cartitem_set.create(product=prod, amount=1)


def category(response, cat_id):
    cat = Category.objects.get(id=cat_id)
    content_type = ContentType.objects.get_for_model(Category)
    items = ShopItem.objects.filter(content_type=content_type, object_id=cat_id)
    button_name = "Default"

    items, button_name = category_sorting(response, items, button_name)
    category_add_to_cart(response)

    return render(response, "mainApp/category.html", {"category": cat, "items": items, "categories": categories, "button_name": button_name})


def subcategory(response, cat_id, subcat_id):
    subcat = Subcategory.objects.get(id=subcat_id)
    content_type = ContentType.objects.get_for_model(Subcategory)
    items = ShopItem.objects.filter(content_type=content_type, object_id=subcat_id)
    button_name = "Default"

    items, button_name = category_sorting(response, items, button_name)
    category_add_to_cart(response)

    return render(response, "mainApp/category.html", {"category": subcat, "items": items, "categories": categories, "button_name": button_name})


def process_payment(response):
    #order_id = request.session.get('order_id')
    #order = get_object_or_404(Order, id=order_id)
    host = response.get_host()
    payment_amount = update_cart_payment_sum(response.user.cart.first())
    invoice_no = response.user.cart.first().id

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': payment_amount, #'%.2f' % order.total_cost().quantize(Decimal('.01')),
        'item_name': "Order no. " + str(invoice_no), #'Order {}'.format(order.id),
        'invoice': invoice_no, #str(order.id),
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(response, 'mainApp/process_payment.html', {'form': form})


@csrf_exempt
def payment_done(response):
    user_cart = response.user.cart.first()

    new_order = Order(user=response.user, number=user_cart.id, total_price=update_cart_payment_sum(user_cart), archival=False)
    new_order.save()
    for item in user_cart.cartitem_set.all():
        new_order.orderitem_set.create(product=item.product, amount=item.amount)

    user_cart.delete()

    response.user.order.add(new_order)

    return render(response, 'mainApp/payment_done.html')


@csrf_exempt
def payment_canceled(response):
    return render(response, 'mainApp/payment_cancelled.html')
