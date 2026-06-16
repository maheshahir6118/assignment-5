from django.contrib import admin
from .models import EmailLog, SMSLog, PaymentLog

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'status', 'sent_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('email',)


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'status', 'sent_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('phone',)


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_id', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('transaction_id',)
