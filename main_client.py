"""
Main runfile for the CARO client-side application.
"""

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
               'darknet':utils.init_environ_darknet()}

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

    return connection.exec_command(command)
