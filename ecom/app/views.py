from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem, Product,Order, OrderItem
# Create your views here.

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

@login_required(login_url='login_with_mfa')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required(login_url='login_with_mfa')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

@login_required(login_url='login_with_mfa')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'cart_detail.html', context)


@login_required(login_url='login_with_mfa')
def process_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    order = Order.objects.create(user=request.user, total_price=cart.total_price)
    for cart_item in cart.cart_items.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, subtotal=cart_item.quantity * cart_item.product.price)
    cart.cart_items.all().delete()
    return redirect('order_confirmation', order_id=order.id)

@login_required(login_url='login_with_mfa')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'order_confirmation.html', context)

