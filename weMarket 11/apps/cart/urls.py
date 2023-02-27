from django.urls import path, include

from apps.cart.views import cart_home, add_to_cart, remove_from_cart
app_name = 'cart'
urlpatterns = [
    path('', cart_home, name='cart_home'),
    path('update/<int:article_id>/', add_to_cart, name='add_to_cart'),
    path('delete/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
]