from apps.product.models import Product, Rate, Category, Size, ProductImage
from django.shortcuts import render, redirect, get_object_or_404
from apps.order.models import Cart, CartItem, Order, Wishlist
from django.contrib.auth.decorators import login_required
from apps.base.models import Variant
from django.http import JsonResponse
from bot.main import order_product
# message
from django.contrib import messages
import asyncio


# Create your views here.

def account(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        "orders": orders
    }
    return render(request, "account.html", context)


def add_to_cart(request):
    ids = 0
    if request.method == "POST":
        session_id = request.session['nonuser']
        product_id = request.POST['product_id']
        product_image = request.POST.get('product_image', None)
        variant = request.POST.get('variant', None)
        quantity = request.POST['quantity']
        size = request.POST.get('size', None)
        cart = get_object_or_404(Cart, session_id=session_id, completed=False)
        product = get_object_or_404(Product, id=product_id)
        has_size = False
        has_color = False
        if product.size.all().exists():
            has_size = True
        if product.product_images.all().exists():
            has_color = True
        if has_color and product_image is not None:
            product_image = product_image.replace(" ", "")
            product_image = get_object_or_404(ProductImage, id=product_image)

        elif has_color and product_image is None:
            return JsonResponse({"msg": "Iltimos! rang tanlang", "status": False})

        if has_size and size is not None:
            size = Size.objects.get(name=size)
        elif has_size and size is None:
            return JsonResponse({"msg": "Iltimos! o'lcham tanlang", "status": False})

        elif variant is None:
            variants = Variant.objects.all().order_by('duration')
            variant = variants.last().id
        variant = get_object_or_404(Variant, id=variant)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id, variant=variant)
        if cart_item.exists():
            for i in cart_item:
                i.quantity += int(quantity)
                i.save()
            ids = cart_item.last().id
        else:
            cart_item = CartItem.objects.create(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                variant=variant
            )
            if size is not None and has_size:
                cart_item.size = size
                cart_item.save()
            if product_image is not None and has_color:
                cart_item.product_image = product_image
                cart_item.save()
            ids = cart_item.id

    return JsonResponse({"msg": "Savatchaga muvaffaqiyatli qo'shildi!", 'card': ids, "status": True})


@login_required(login_url='/login')
def create_order(request, id):
    phone_number = request.POST.get("phone_number", False)
    cart = get_object_or_404(Cart, id=id)
    cart_items = cart.cart_items.all()
    user = request.user
    order = Order.objects.create(
        user=user,
        phone_number=user.username
    )
    for item in cart_items:
        item.order = order
        item.save()

    cart.completed = True
    cart.save()
    data = []
    for i in cart_items:
        data.append(dict(
            order=order.id,
            user=request.user.username,
            product=i.product.title,
            quantity=i.quantity,
            variant=i.variant.duration,
            photo=i.product_image.image.url
        ))
    print(data)
    asyncio.run(order_product(data))

    return redirect('/')


def one_click_order(request):
    phone_number = request.POST.get("phone_number", None)
    product_id = request.POST.get("product_id", None)
    quantity = request.POST.get("quantity", None)
    variant = request.POST.get("variant", None)
    size = request.POST.get("size", None)
    product_image = request.POST.get("product_image", None)
    user = request.user

    print(product_image, 'product_image')

    product = get_object_or_404(Product, id=product_id)


    if phone_number is None:
        return JsonResponse({"msg": "Iltimos, telefon raqamni kiriting!", "status": False})

    if variant is None:
        return JsonResponse({"msg": "Iltimos, variantni tanlang!", "status": False})

    if product_id is None:
        return JsonResponse({"msg": "Iltimos, mahsulotni tanlang!", "status": False})

    cart = Cart.objects.create(
        session_id=request.session['nonuser'],
        completed=True
    )
    order = Order()
    if user.is_authenticated:
        order.user = user
        order.phone_number = phone_number
    else:
        order.phone_number = phone_number
    order.save()
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(Variant, id=variant)
    if size:
        size = get_object_or_404(Size, name=size)
    if product_image:
        product_image = get_object_or_404(ProductImage, id=product_image)
    cart_item = CartItem.objects.create(
        cart=cart,
        order=order,
        product=product,
        quantity=quantity,
        variant=variant,
        size=size,
        product_image=product_image
    )
    cart_item.save()
    data = []

    data.append(dict(
        user=phone_number,
        order=order.id,
        product=cart_item.product.title,
        quantity=cart_item.quantity,
        variant=cart_item.variant.duration,
        photo=cart_item.product_image.image.url
    ))
    asyncio.run(order_product(data))

    return redirect('/')


def confirm_order(request):
    id = request.POST.get("id", False)
    phone_number = request.POST.get("phone_number", False)

    cart = get_object_or_404(Cart, id=id)
    cart_items = cart.cart_items.all()

    user = request.user
    if user.is_authenticated:
        order = Order.objects.create(
            user=user,
            phone_number=f"{user} | {phone_number}"
        )
    else:
        order = Order.objects.create(
            phone_number=phone_number
        )
    for item in cart_items:
        item.order = order
        item.save()

    cart.completed = True
    cart.save()
    data = []
    for i in cart_items:
        data.append(dict(
            user=phone_number,
            order=order.id,
            product=i.product.title,
            quantity=i.quantity,
            variant=i.variant.duration,
            photo=i.product_image.image.url
        ))
    asyncio.run(order_product(data))

    return redirect('/')


@login_required(login_url='/login')
def review(request):
    rating = request.POST['rating']
    comment = request.POST['comment']
    product = request.POST['product']
    user = request.user

    rate = Rate.objects.create(
        user=user,
        product_id=product,
        comment=comment,
        rate=rating
    )
    return redirect(f'/shop-details/{product}')


def shop_cart(request):
    session_id = request.session['nonuser']
    cart = Cart.objects.filter(session_id=session_id, completed=False)
    category = Category.objects.all()
    context = {
        'cart': cart.last(),
        'categories': category[10:],
        'hide_categories': category[10:],
    }
    return render(request, "shop-cart.html", context)


def delete_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.delete()
    return redirect('/order/shop-cart')


def wishlist(request, id):
    session_id = request.session['nonuser']
    product = get_object_or_404(Product, id=id)
    url = request.META.get('HTTP_REFERER')

    if Wishlist.objects.filter(session_id=session_id, product=product).exists():
        return redirect(url)
    else:
        wishlist = Wishlist.objects.create(
            session_id=session_id,
            product=product
        )
        return redirect(url)


def wishlist_list(request):
    return render(request, "shop-wishlist.html")


def delete_wishlist(request, id):
    Wishlist.objects.get(id=id).delete()
    url = request.META.get('HTTP_REFERER')
    return redirect(url)


def create_order_wishlist(request, id):
    product = Product.objects.get(id=id)
    session_id = request.session['nonuser']
    cart = Cart.objects.get(session_id=session_id, completed=False)
    cart_item = CartItem.objects.create(
        product=product,
        quantity=1,
        cart=cart
    )
    wishlist = Wishlist.objects.filter(session_id=session_id, product_id=id).delete()
    url = request.META.get('HTTP_REFERER')
    return redirect(url)
