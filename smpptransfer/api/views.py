from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from smpptransfer.api.serializers import InboundMessageSerializer, SendCommandSerializer, \
    InboundMessageResourceSerializer
from smpptransfer.models import InboundMessage, SendCommand
from smpptransfer.utils.sender_helper import init_message_send
from smpptransfer.utils.reader_helper import mark_messages_as_read


@csrf_exempt
@api_view(['GET'])
def read_unread_messages(request):
    """
        Returns un-retrieved messages
    """
    messages = InboundMessage.objects.order_by("created_at").filter(is_retrieved=False).all()
    serializer = InboundMessageResourceSerializer(messages, many=True)

    # mark messages as retrieved now
    # This is done a in a background job
    if len(messages) is not 0:
        mark_messages_as_read(messages.first().id, messages.last().id)

    data = {
        "messages": serializer.data
    }

    return Response(data)


@csrf_exempt
@api_view(['GET'])
def read_all_messages(request):
    """
        Returns all messages
    """
    messages = InboundMessage.objects.order_by("created_at").all()
    serializer = InboundMessageResourceSerializer(messages, many=True)

    data = {
        "messages": serializer.data
    }
    return Response(data)


@csrf_exempt
@api_view(['POST'])
def send_messages(request):
    """"
        Send messages
    """
    serializer = SendCommandSerializer(data=request.POST)

    if serializer.is_valid():
        content = serializer.validated_data.get('content')
        source = serializer.validated_data.get('source')
        destination = serializer.validated_data.get('destination')

        send_command = SendCommand(content=content, destination=destination)

        if source:
            send_command.source = source

        send_command.save()

        init_message_send(send_command.id)
        return Response({"status": "ok"})

    return Response({"status": "bad", "errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
