from django.contrib import admin

from smpptransfer.models import InboundMessage, OutboundMessage, SendCommand

admin.site.site_header = 'SMS Adapter'


@admin.register(InboundMessage)
class InboundMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'received_at', 'is_retrieved', 'retrieved_at', 'created_at', 'msg_type')


@admin.register(OutboundMessage)
class OutboundMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'source', 'network', 'destination', 'delivery_status', 'received_at', 'is_sent', 'sent_at', 'attempts',
        'created_at',)


@admin.register(SendCommand)
class SendCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'received_at', 'is_queued', 'is_processed', 'created_at', 'updated_at')
