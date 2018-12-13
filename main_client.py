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
