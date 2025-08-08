from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('initiate-payment/', views.InitiatePaymentView.as_view(), name='initiate_payment'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
]
