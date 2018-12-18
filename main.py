"""
Main handler for the catcher_rover server component.
"""

import os
import logging

import utils
import socks
import pydarknet as pdn


def init_environ():
    """Initialize environment parameters.

    Args:
        None

    Returns:
        A dictionary containing all environment variables.
    """

    caro_loc, inbox_loc = utils.init_environ_folder()

    environ = {'caro_loc':caro_loc,
               'inbox_loc':inbox_loc,
               'net':utils.init_environ_net(),
               'darknet':utils.init_environ_darknet(),
               'debug': os.environ['DEBUG']}

    return environ


def darknet_model(cfg, weight, data):
    """Initialize Darknet model.

    Args:
        cfg: A string representing the cfg file path.
        weight: A string representing the weight file path.
        data: A string representing the data file path.

    Returns:
        A Darknet model tuple: (model, network, metadata).
    """

    dark = pdn.Pydarknet('libdarknet.so')

    load_network = dark.init_load_net()
    network = load_network(cfg.encode(), weight.encode(), 0)

    load_metadata = dark.init_load_meta()
    metadata = load_metadata(data.encode())

    return (dark, network, metadata)


def start_server():
    """Runs the catcher_rover main loop."""

    environ = init_environ()

    utils.init_logger(environ['debug'])
    logger = logging.getLogger('__main__')
    logger.info("catcher_rover server - hello")

    logger.info("initializing darknet model")
    dark, network, metadata = darknet_model(environ['darknet']['cfg'],
                                            environ['darknet']['weights'],
                                            environ['darknet']['data'])

    logger.info("initializing server socket")
    server_socket = socks.init_server_socket()

    while True:
        server_socket.listen(5)
        logger.info("waiting for incoming connections")
        client, addr = server_socket.accept()
        logger.info("incoming connection from %s", str(addr))

        logger.info("receiving frames")

        frame_size = int(socks.receive_bytes_to_string(client))
        socks.send_msg(client, 'OK FRAME')
        socks.receive_frame(client, frame_size, environ['inbox_loc'])
        logger.info("frame received")

        logger.info("starting label detection")

        image = os.path.join(environ['inbox_loc'], "frame.jpg")
        results = dark.detect((network, metadata, image.encode()))

        logger.info("sending frame received ack")
        socks.send_msg(client, 'OK FRAME')

        logger.info("frame processing completed")

        logger.info("sending bounding boxes")
        logger.info("bounding box values: %s", str(results))
        socks.waiting_for_ack(client, "VECT")
        socks.send_msg(client, results)

        logger.info("results sent")

        logger.info("closing sockets")
        client.close()


if __name__ == '__main__':
    start_server()
