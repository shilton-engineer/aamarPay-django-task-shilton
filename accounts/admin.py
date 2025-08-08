from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FileUpload, ActivityLog, PaymentTransaction

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'filename', 'upload_time', 'status', 'word_count')
    readonly_fields = ('user', 'filename', 'upload_time', 'status', 'word_count','file')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    readonly_fields = ('user', 'action', 'metadata', 'timestamp')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'status', 'timestamp')
    readonly_fields = ('user', 'transaction_id', 'amount', 'status', 'gateway_response', 'timestamp')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
