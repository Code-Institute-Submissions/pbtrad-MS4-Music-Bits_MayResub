from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from coupons.models import Coupon

def cart_contents(request):

    cart_items = []
    sub_total = 0
    total = 0
    discount_total = 0
    discount_percentage = 0
    product_count = 0
    cart = request.session.get('cart', {})
    coupon_id = request.session.get('coupon_id', int())

    try:
        code = Coupon.objects.get(id=coupon_id)

    except Coupon.DoesNotExist:
        code = None

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            sub_total += item_data * product.price
            total += item_data * product.price
            product_count += item_data

            if code is not None:
                discount_percentage = code.discount
                discount_total = (discount_percentage/Decimal('100'))*sub_total
                total = sub_total - discount_total
            else:
                total = sub_total

            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += int(quantity) * int(product.price)
                product_count += int(quantity)
                cart_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'sub_total': sub_total,
        'code': code,
        'discount_total': discount_total,
        'discount_percentage': discount_percentage,
        'grand_total': grand_total,
    }

    return context