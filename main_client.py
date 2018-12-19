"""
Main runfile for the CARO client-side application.
"""

import os
import logging

import utils
import camera
import net
import socks


def init_environ():
    """Initialize environment parameters.

    Args:
        None

    Returns:
        A dictionary containing all environment variables.
    """

    environ = {'capture_loc':utils.init_environ_folder(),
               'net':utils.init_environ_net(),
               'darknet':utils.init_environ_darknet(),
               'debug':os.environ['DEBUG']}

    return environ


def start_cloud_instance(cloud, instance, network, volume):
    """Starts a cloud instance.

    Args:
        cloud: A string defining the cloud to connect to.
        instance: A dict with instance details.
        net: A dict with net details.
        volume: A dict with volume details.

    Returns:
        The created Cloud instance.
    """

    target_cloud = net.Cloud(cloud, instance, network, volume)

    target_cloud.create_instance()

    return target_cloud


def run_cloud_command(remote_ip, username, keyfile, command, retry=10):
    """Executes an arbitraty command on the cloud instance and retrieve
    output.

    Args:
        remote_ip: A string representing the remote IP to connect to.
        username: A string representing the username to employ.
        keyfile: A string representing the keyfile path.
        retry: An int representing the number of ssh connection attemps to do.
        command: A string representing the remote command to execute.

    Returns:
        A tuple including std streams (stdin, stdout, stderr).
    """

    connection = net.Ssh(remote_ip, username, keyfile)

    connection.remote_connect(retry)

    return (connection, connection.exec_command(command))


def run_catcher_rover():
    """Runs the catcher_rover main loop."""

    environ = init_environ()

    utils.init_logger(environ['debug'])
    logger = logging.getLogger('__name__')

    cloud = start_cloud_instance(environ['net']['cloud_name'],
                                 environ['net']['instance'],
                                 environ['net']['nets'],
                                 environ['net']['volume'])

    command = ("echo 'nameserver 8.8.8.8' |" +
               " sudo tee /etc/resolv.conf > /dev/null" +
               " cd /opt" +
               " ; sudo git clone https://github.com/julienstark/catcher_rover.git" +
               " ; cd catcher_rover ; sudo git checkout origin/darknet-api" +
               " ; sudo mv ../darknet/ ./" +
               " ; sudo systemctl start caroserver.service")

    connection, output = run_cloud_command(environ['net']['nets']['ips'],
                                           environ['net']['username'],
                                           environ['net']['keyfile'],
                                           command)

    if output[2] is not None:
        logger.error("error caught on instance command: %s", output[2].readlines())

    output[1].readlines()

    connection.client.close()
    cam = camera.Camera(environ['capture_loc'])

    client_socket = socks.init_client_socket(environ['net']['nets']['ips'])

    for count in range(10):

        logger.info("iteration %s, capturing frame", str(count))
        cam.capture()
        logger.info("frame captured")

        logger.info("sending frame")
        frame_loc = os.path.join(environ['capture_loc'] + "frame.jpg")
        socks.send_frame_size(client_socket, frame_loc)
        socks.waiting_for_ack(client_socket)
        socks.send_frame(client_socket, frame_loc)
        logger.info("waiting for frame reception")
        socks.waiting_for_ack(client_socket)

        logger.info("frame sent")

        logger.info("receiving vector")

        socks.send_msg(client_socket, "OK VECT")
        recv_string = socks.receive_bytes_to_string(client_socket)
        recv_string = recv_string.replace(", ", " ").replace(": ", ":")
        recv_string = recv_string.strip("{}").replace("'", "")
        os.remove(frame_loc)

        logger.info("vector received")

        if recv_string != "":

            # Do the robot move here
            pass

        else:
            logger.warning("no detection for this frame")

        cloud.delete_instance()


if __name__ == '__main__':
    run_catcher_rover()
