import smpplib.gsm
import smpplib.client
import smpplib.consts
from background_task import background

from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.conf import settings

from smpptransfer.models import SendCommand, OutboundMessage


def establish_client_connection(client_key):
    """
    Binds the client as a transmitter
    Establishes a connection with an SMPP server and returns the client connection
    :param client_key:
    :return:
    """
    try:
        client_config = settings.SMPP_CONNECTIONS[client_key]

        client = smpplib.client.Client(client_config["host"], client_config["port"], allow_unknown_opt_params=True)
        client.connect()

        client.bind_transmitter(system_id=client_config["system_id"],
                                password=client_config["password"],
                                system_type=client_config["system_type"])

        return client
    except:
        return None


@background(queue="messages-queue")
def init_message_send(send_command_id, client_connections=None):
    """
    Initiates sending of text SMS to the destination numbers in the send command
    It takes a send command id to retrieve the send command to get the content and destination numbers
    :param client_connections:
    :param send_command_id:
    :return:
    """
    send_command = SendCommand.objects.filter(id=send_command_id).first()

    if send_command is None:
        return None

    message = send_command.content
    numbers = send_command.destination.split(",")

    # establish connection to SMPP servers
    if client_connections is None:
        client_connections = ["airtel", "tnm"]

    clients = {}

    for client_connection in client_connections:
        clients[client_connection] = establish_client_connection(client_connection)

    source_number = "3344"

    send_command.is_queued = True
    send_command.is_processed = True

    try:
        for number in numbers:
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts((u"{}".format(message)) * 1)

            # determine client
            client = None
            network = None

            if "2659" in number:
                network = "airtel"
            elif "2658" in number:
                network = "tnm"

            if network in client_connections:
                client = clients[network]

            # Record atomic message
            msg = OutboundMessage(
                content=message,
                source=source_number,
                destination=number,
                network=network,
                sent_at=datetime.now(tz=get_current_timezone()),
                received_at=datetime.now(tz=get_current_timezone()),
                created_at=datetime.now(tz=get_current_timezone()),
                updated_at=datetime.now(tz=get_current_timezone())
            )

            msg.save()

            if client is None:
                # we do not know how to send this number
                # leave it as un sent
                continue

            # Send actual message data
            for part in parts:
                # Send message
                client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    source_addr=source_number,
                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    destination_addr=number,
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )

            msg.is_sent = True
            msg.save()
    except:
        send_command.is_processed = False  # mark this send command as not fully processed
        pass

    send_command.save()

    for client_connection in client_connections:
        if clients[client_connection] is not None:
            clients[client_connection].unbind()


def init_sending_scheduled_messages(client_connections=None):
    """
    Sends out any unsent messages
    :return:
    """
    unsent_messages = OutboundMessage.objects.filter(is_sent=False, attempts__lt=settings.SMPP_SEND_MAX_ATTEMPTS).all()

    # establish connection to SMPP servers
    if client_connections is None:
        client_connections = ["airtel", "tnm"]

    clients = {}

    for client_connection in client_connections:
        clients[client_connection] = establish_client_connection(client_connection)

    source_number = "3344"

    try:
        for message in unsent_messages:
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts((u"{}".format(message.content)) * 1)

            number = message.destination

            # determine client
            client = None
            network = message.network

            if network in client_connections:
                client = clients[network]

            message.sent_at = datetime.now(tz=get_current_timezone())
            message.attempts += 1
            message.save()

            if client is None:
                # we do not know how to send this number
                # leave it as un sent
                continue

            # Resend Send actual message data
            for part in parts:
                # Send message
                client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    source_addr=source_number,
                    source_npi=smpplib.consts.SMPP_NPI_UNK,
                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    destination_addr=number,
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )

            message.is_sent = True
            message.save()
    except:
        pass

    # unbind any connection
    for client_connection in client_connections:
        if clients[client_connection] is not None:
            clients[client_connection].unbind()
