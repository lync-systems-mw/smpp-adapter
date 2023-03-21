from datetime import datetime

from django.db import models


class InboundMessage(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    source = models.CharField(max_length=15)
    is_retrieved = models.BooleanField(default=False)
    retrieved_at = models.DateTimeField(null=True)
    msg_type = models.CharField(max_length=20, choices=[("delivery", "Delivery"), ("normal", "Normal")],
                                default="normal")
    received_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


class OutboundMessage(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    source = models.CharField(max_length=15)
    network = models.CharField(max_length=30, null=True)
    destination = models.CharField(max_length=15)
    is_sent = models.BooleanField(default=False)
    attempts = models.IntegerField(default=1)
    delivery_status = models.IntegerField(default=0)
    received_at = models.DateTimeField(default=datetime.now)
    delivered_at = models.DateTimeField(null=True)
    sent_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


class SendCommand(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    source = models.CharField(default="Chiweto", max_length=30)
    destination = models.TextField()
    received_at = models.DateTimeField(default=datetime.now)
    is_queued = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
