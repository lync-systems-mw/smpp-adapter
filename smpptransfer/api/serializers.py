from rest_framework import serializers

from smpptransfer.models import InboundMessage, SendCommand


class InboundMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundMessage
        fields = "__all__"


class InboundMessageResourceSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="source")
    date_time = serializers.SerializerMethodField()
    text = serializers.ReadOnlyField(source="content")

    def get_date_time(self, obj):
        return obj.received_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InboundMessage
        fields = ['text', 'sender', "id", "date_time"]


class SendCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendCommand
        fields = "__all__"
