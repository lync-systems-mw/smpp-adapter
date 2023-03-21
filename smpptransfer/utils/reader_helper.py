from datetime import datetime

import smpplib.gsm
import smpplib.client
import smpplib.consts

from smpptransfer.models import InboundMessage
from django.conf import settings

from threading import Thread
from background_task import background

from django.utils.timezone import get_current_timezone


def establish_client_connection(client_key):
    """
    Binds the client as a receiver
    :param client_key:
    :return:
    """
    client_config = settings.SMPP_CONNECTIONS[client_key]

    client = smpplib.client.Client(client_config["host"], client_config["port"], allow_unknown_opt_params=True)
    client.connect()

    client.bind_receiver(system_id=client_config["system_id"],
                         password=client_config["password"],
                         system_type=client_config["system_type"])

    client.set_message_received_handler(lambda pdu: receive_message(pdu))

    return client


def init_messages_listen(client_connections=None):
    """
       Initiates listening for SMPP server events
       :return:
       """

    if client_connections is None:
        client_connections = ["airtel", "tnm_receiver_1", "tnm_receiver_2"]

    clients = []

    for client_connection in client_connections:
        client = establish_client_connection(client_connection)

        if client is not None:
            client_thread = Thread(target=client.listen)
            client_thread.start()

    # for client in clients:
    #     client_thread = Thread(target=client.listen)
    #     client_thread.start()

    # # read from airtel
    # airtel_client = establish_client_connection("airtel")
    #
    # airtel_thread = Thread(target=airtel_client.listen)
    # airtel_thread.start()


def init_messages_fetch(client_connections=None):
    """
    Initiates retrieval of messages from an SMSC servers given in the connections list
    :param client_connections:
    :return:
    """

    if client_connections is None:
        client_connections = ["airtel", "tnm_receiver_1", "tnm_receiver_2"]

    # for each client connection establish a connection and read all available message
    # Then disconnect
    for client_connection in client_connections:
        client = establish_client_connection(client_connection)

        # Continue with next client connection if the connection
        # For this one could not be established
        if client is None:
            print("Could not establish connection for :{}".format(client_connection))
            continue

        while True:
            try:
                pdu = client.read_pdu()
                receive_message(pdu)
            except:
                print("Could not read any more PDUs... breaking now")
                break

        client.unbind()


def receive_message(pdu):
    """
    Accepts received PDU and processes it into a valid Inbound Message,
    If it is not a delivery message
    :param pdu:
    :return:
    """

    if pdu is not None:
        message = pdu.short_message.decode("utf-8")
        source = pdu.source_addr.decode("utf-8")

        inbound_message = InboundMessage(content=message, source=source)

        # check if this is not delivery message
        # set the appropriate message type
        if "dlvrd" not in inbound_message.content:
            inbound_message.save()

    else:
        print("PDU is none")


@background(queue="retrieval-queue")
def mark_messages_as_read(start_id, last_id):
    """
    Marks messages as retrieved
    Takes the id of the first message in the list and id of the last message
    :param start_id:
    :param last_id:
    :return:
    """
    InboundMessage.objects.filter(id__lte=last_id).filter(id__gte=start_id).update(
        is_retrieved=True,
        retrieved_at=datetime.now(tz=get_current_timezone())
    )
