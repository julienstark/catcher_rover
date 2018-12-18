"""
Module supporting various functions responsible for initiating and managing
socket connections between a client and a server.

function init_client_socket: Initialize client socket.

function init_server_socket: Initialize server socket.

function receive_bytes_to_string: Convert incoming messages from bytes to str.

function send_frame_size: Send frame size to client.

function send_frame: Send frame to client.

function receive_frame: Receive and save one frame.

function waiting_for_ack: Wait for a particular frame/message to be acked by
server.

function send_msg: Send arbitrary message to the peer.
"""

import socket
import os

import netifaces as ni


def init_client_socket(address, port=5000):
    """Initialize client socket.

    Args:
        address: string representing the IP address to connect to.
        port: Optional int representing the port to connect to.

    Returns:
        A client socket where the program can start sending messages.
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    return client_socket


def init_server_socket(address=None, port=5000):
    """Initialize server socket.

    Args:
        address: Optional string representing the IP address to bind to.
        port: Optional int representing the port to connect to.

    Returns:
        A server socket where the program can receive messages.
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if address is None:
        address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((address, port))

    return server_socket


def receive_bytes_to_string(client_sock):
    """Convert incoming messages from bytes to str.

    Receives message first, then do the byte to str translation.

    Args:
        client_sock: A socket instance representing the client socket.

    Returns:
        None
    """

    byte_msg = client_sock.recv(1024)
    str_msg = byte_msg.decode('utf-8').replace("\n", "")

    return str_msg


def send_frame_size(client_socket, frame_loc):
    """Send frame size to client.

    Function useful for the server since it will use this result to compute
    frame size and bytes reception accordingly. With this number, a
    server can exactly knows how many bytes to expect from a stream flow in
    order to fully receive a frame.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        frame_loc: A string representing the frame location to compute and
        send size from.

    Returns:
        None
    """

    filesize = os.path.getsize(frame_loc)
    client_socket.send(str(filesize).encode('ascii'))


def send_frame(client_socket, frame_loc):
    """Send frame to client.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        frame_loc: A string representing the frame location.

    Returns:
        None
    """

    with open(frame_loc, 'rb') as filedesc:
        buf = filedesc.readline(1024)
        while buf:
            client_socket.send(buf)
            buf = filedesc.readline(1024)
        filedesc.close()


def receive_frame(client_sock, frame_size, save_loc):
    """Receive and save one frame.

    Main function responsible for storing and saving exactly one frame from
    a remote client. In order to properly delimitate a frame from a stream,
    the function also takes the frame size as a parameter and compute the
    necessary incoming byte number to expect.

    Args:
        client_sock: A socket instance representing a client connection.
        frame_size: An int representing the frame size to expect.
        save_loc: A string representing the destination where to save the
        frame

    Returns:
        None
    """

    img_size = 0
    filename = save_loc + "frame.jpg"
    with open(filename, 'wb') as img:
        while img_size < frame_size:
            remain = frame_size - img_size
            if remain < 1024:
                data = client_sock.recv(remain)
            else:
                data = client_sock.recv(1024)
            img.write(data)
            img_size += len(data)


def waiting_for_ack(client_socket, exptype='FRAME'):
    """Wait for a particular frame/message to be acked by server.

    Args:
        client_socket: A socket instance, used for client/server interactions.
        exptype: A string representing the type of ack to wait for.

    Returns:
        None
    """

    msg = client_socket.recv(1024).decode('UTF-8')
    while msg != 'OK ' + exptype:
        msg = client_socket.recv(1024).decode('UTF-8')


def send_msg(client_sock, msg):
    """Send message to the peer.

    Args:
        client_sock: A socket instance representing the client connection.
        msg: An string representing the message to send.

    Returns:
        None
    """

    client_sock.send((str(msg)).encode('ascii'))
