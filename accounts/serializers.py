from rest_framework import serializers
from .models import FileUpload, ActivityLog, PaymentTransaction

class InitiatePaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file']

class FileUploadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'filename', 'upload_time', 'status', 'word_count']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'action', 'metadata', 'timestamp']

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'transaction_id', 'amount', 'status', 'timestamp']

