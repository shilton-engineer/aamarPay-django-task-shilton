from django.urls import path
from . import views
from .views import (
    FileUploadListView,
    ActivityLogListView,
    PaymentTransactionListView,
)

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('initiate-payment/', views.InitiatePaymentView.as_view(), name='initiate_payment'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('files/', FileUploadListView.as_view(), name='file-list'),
    path('activity/', ActivityLogListView.as_view(), name='activity-list'),
    path('transactions/', PaymentTransactionListView.as_view(), name='transaction-list'),
]


