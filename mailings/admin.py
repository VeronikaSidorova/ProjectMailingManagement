from django.contrib import admin
from .models import Recipient, Message, Campaign, SendAttempt, SendLog

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    search_fields = ('full_name', 'email')
    list_filter = ('comment',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time')
    list_filter = ('status',)
    search_fields = ('id',)
    date_hierarchy = 'start_time'
    filter_horizontal = ('recipients',)  # чтобы удобно выбирать получателей

@admin.register(SendAttempt)
class SendAttemptAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'attempt_time', 'status')
    list_filter = ('status',)
    search_fields = ('campaign_id',)

@admin.register(SendLog)
class SendLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'campaign', 'attempt_time', 'status')
    list_filter = ('status',)
    search_fields = ('recipient__full_name', 'campaign_id')