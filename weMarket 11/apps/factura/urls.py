from django.urls import path, include

from .views import Credit_card, Checkout, Success, Not_money, Review_bill, Bill_value, Change_qty

app_name = 'billing'

urlpatterns = [
    path('credit_card/', Credit_card, name='credit_card'),
    path('checkout/', Checkout, name='checkout'),
    path('success_checkout/', Success, name='success_checkout'),
    path('not_money/', Not_money, name='not_money'),
    path('review_bill/<int:id_bill>/', Review_bill, name='review_bill'),
    path('bill_value/<int:id_bill>/', Bill_value, name='bill_value'),
    path('change_qty/', Change_qty, name='change_qty'),
]