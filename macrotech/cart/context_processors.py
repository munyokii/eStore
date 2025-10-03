"""Cart Context Processor """
def cart_count(request):
    """Cart context processor function"""
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return {'cart_count': count}
