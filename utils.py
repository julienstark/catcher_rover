"""
Module supporting various helpers and utility functions.

function init_logger: Initialize the logger function.

function init_environ_folder: Return necessary variables based on environment.

class SuppressStdOutput: Suppress embedded function outputs.
"""

import os
import inspect
import logging


def init_logger(appname):
    """Initialize the logger function for the project.

    Args:
        appname: A string representing the name of the app to log for.

    Returns:
        A log object handling various logging messages.
    """

    logfile = os.path.join(os.environ['CARO_LOGFILE'])
    logging.basicConfig(filename=logfile,
                        filemode="w",
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                        datefmt='%b %d %H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logging.getLogger("").addHandler(console)

    return logging.getLogger(appname)


def init_environ_folder():
    """Return necessaru capture_loc/inbox, caro_loc based on environ.

    Variable capture_loc is used to determine where frames captured by the
    Camera class resides.
    Variable inbox_loc indicates where incoming frames are saved and variable
    caro_loc indicates the path of the project folder.

    Args:
        None

    Returns:
        Strings representing either capture_loc if the caller is the client, a
        tuple with caro_loc and inbox_loc otherwise.
    """

    stackp = inspect.stack()[1]
    module = inspect.getmodule(stackp[0])
    caller_filename = module.__file__

    if caller_filename == 'main_client.py':
        capture_loc = os.path.join(os.environ['CARO_CAPTURE_FOLDER'])
        return capture_loc

    caro_loc = os.environ['CARO_FOLDER']
    inbox_loc = os.environ['CARO_INBOX_FOLDER']

    return caro_loc, inbox_loc


def init_environ_net():
    """Return necessary cloud and ssh configs, based on environ.

    Cloud-related variables define cloud access logic and instance params.
    SSH-related variables describe how to connect to a remote instance.

    This function should only be used on the client-side of the application.

    Args:
        None

    Returns:
        A tuple containing: (string cloud_config, string cloud_name,
        dict instance, dict nets, dict volume, string username, string keyfile)
    """

    cloud_config = os.environ['CARO_CLOUD_CONFIG_FILE']
    cloud_name = os.environ['CARO_CLOUD_NAME']

    instance = {'name':os.environ['CARO_CLOUD_INSTANCE_NAME'],
                'image':bool(os.environ['CARO_CLOUD_INSTANCE_IMAGE']),
                'flavor':os.environ['CARO_CLOUD_INSTANCE_FLAVOR']}

    nets = {'security_groups':os.environ['CARO_CLOUD_INSTANCE_SECURITY_GROUPS'],
            'network':os.environ['CARO_CLOUD_INSTANCE_NETWORK'],
            'ips':os.environ['CARO_CLOUD_INSTANCE_IP']}

    volume = {'boot_volume':os.environ['CARO_CLOUD_INSTANCE_BOOT_VOLUME'],
              'volume_size':os.environ['CARO_CLOUD_INSTANCE_VOLUME_SIZE']}

    username = os.environ['CARO_CLOUD_SSH_USERNAME']
    keyfile = os.environ['CARO_CLOUD_SSH_KEYFILE']

    return (cloud_config, cloud_name, instance, nets, volume, username, keyfile)


def init_environ_darknet():
    """Return necessary darknet variables, based on environ params.

    Explicits darknet folder, darknet configuration file, weight, data and
    label to use.

    Args:
        None

    Returns:
        A tuple containing: (string darknet_folder, string darknet_label,
        string darknet_cfg, string darknet_weights, string darknet_data)
    """

    darknet_folder = os.environ['CARO_DARKNET_FOLDER']
    darknet_label = os.environ['CARO_DARKNET_LABEL']
    darknet_cfg = os.environ['CARO_DARKNET_CFG']
    darknet_weights = os.environ['CARO_DARKNET_WEIGHTS']
    darknet_data = os.environ['CARO_DARKNET_DATA']

    return (darknet_folder, darknet_label, darknet_cfg, darknet_weights,
            darknet_data)


class SuppressStdOutput():
    """Wrapper used for doing 'deep suppression' of stdout and stderr of a
    function. Does not affect raised exceptions.

    Attributes:
        null_fds = A list containing a pair of null file descriptors.
        save_fds = A list containing saved stdout and stderr file desc.
    """

    def __init__(self):
        """Default class builder."""

        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        self.save_fds = [os.dup(1), os.dup(2)]


    def __enter__(self):
        """Assign the null pointers to sdtout and stderr.

        Args:
            None

        Returns:
            None
        """

        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)


    def __exit__(self, *_):
        """Re-assign the real stdout/stderr back to (1) and (2).

        Args:
            None

        Returns:
            None
        """

        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)

        for fdesc in self.null_fds + self.save_fds:
            os.close(fdesc)
