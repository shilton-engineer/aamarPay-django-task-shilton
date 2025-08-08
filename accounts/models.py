from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PaymentTransaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=50)
    gateway_response = models.JSONField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.user}"


class FileUpload(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='processing')
    word_count = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.filename} uploaded by {self.user}"


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    metadata = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"







