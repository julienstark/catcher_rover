"""
Module supporting various helpers and utility functions.

function init_logger: Initialize the logger function.

function init_environ_folder: Return necessary variables based on environment.

function get_image_size: Get image size pixel W and H from filepath.

class SuppressStdOutput: Suppress embedded function outputs.
"""

import os
import inspect
import logging
import struct
import imghdr


def init_logger(debug):
    """Initialize the logger function for the project.

    Args:
        debug: A bool defining debug mode (verbose output) or not.

    Returns:
        None
    """

    logfile = os.path.join(os.environ['CARO_LOGFILE'])
    logging.basicConfig(filename=logfile,
                        filemode="w",
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                        datefmt='%b %d %H:%M:%S')

    console = logging.StreamHandler()

    if debug == 'True':
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.ERROR)

    logging.getLogger("").addHandler(console)


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
        A dict containing: {string cloud_config, string cloud_name,
        dict instance, dict nets, dict volume, string username, string keyfile}
    """

    cloud_config = os.environ['CARO_CLOUD_CONFIG_FILE']
    cloud_name = os.environ['CARO_CLOUD_NAME']

    instance = {'name':os.environ['CARO_CLOUD_INSTANCE_NAME'],
                'image':os.environ['CARO_CLOUD_INSTANCE_IMAGE'],
                'flavor':os.environ['CARO_CLOUD_INSTANCE_FLAVOR']}

    nets = {'security_groups':os.environ['CARO_CLOUD_INSTANCE_SECURITY_GROUPS'],
            'network':os.environ['CARO_CLOUD_INSTANCE_NETWORK'],
            'ips':os.environ['CARO_CLOUD_INSTANCE_IP']}

    volume = {'boot_volume':os.environ['CARO_CLOUD_INSTANCE_BOOT_VOLUME'],
              'volume_size':os.environ['CARO_CLOUD_INSTANCE_BOOT_VOLUME_SIZE']}

    username = os.environ['CARO_CLOUD_SSH_USERNAME']
    keyfile = os.environ['CARO_CLOUD_SSH_KEYFILE']

    net_environ = {'cloud_config':cloud_config,
                   'cloud_name':cloud_name,
                   'instance':instance,
                   'nets':nets,
                   'volume':volume,
                   'username':username,
                   'keyfile':keyfile}

    return net_environ


def init_environ_darknet():
    """Return necessary darknet variables, based on environ params.

    Explicits darknet folder, darknet configuration file, weight, data and
    label to use.

    Args:
        None

    Returns:
        A dict containing: {string darknet_folder, string darknet_label,
        string darknet_cfg, string darknet_weights, string darknet_data}
    """

    darknet_environ = {'folder':os.environ['CARO_DARKNET_FOLDER'],
                       'label':os.environ['CARO_DARKNET_LABEL'],
                       'cfg':os.environ['CARO_DARKNET_CFG'],
                       'weights':os.environ['CARO_DARKNET_WEIGHTS'],
                       'data':os.environ['CARO_DARKNET_DATA']}

    return darknet_environ


def get_image_size(fname):
    """Determine the image type of fhandle and return its size.

     Args:
        fname: A string representing the image path

    Returns:
        A tuple including the image pixel width and height.
    """

    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return None
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return None
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #pylint: disable=broad-except
                return None
        else:
            return None
        return width, height


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
