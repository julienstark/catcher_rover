#pylint: disable=import-error
"""
Module supporting the Rover class, responsible for handling and representing
various core rover vehicle functions, such as movement and various ardupilot
functionalities.

function initialize_vehicle: starts a serial connection to the rover and returns
a Vehicle instance.

class Rover: contains the builder and the main rover navigation functions.

"""


import time
import logging

import dronekit


def initialize_vehicle(connection_string, baud):
    """Connects to an APM / PixHawk board via 'connection_string'.

    Args:
        connection_string = A string representing the connection medium to the
        board http://python.dronekit.io/guide/connecting_vehicle.html.
	baud = An int representing the connection baud rate.

    Returns:
	A Vehicle instance.
    """

    vehicle = dronekit.connect(connection_string, wait_ready=False, baud=baud)

    return vehicle


class Rover:
    """Class responsible for handling the Rover navigation and management functions.

    Direct interface with the embarked APM / PixHawk board supporting Ardupilot
    navigation functions.

    Attributes:
        vehicle: A Vehicle instance representing the physical rover.
        rest_time: An int representing the rest time between two MAVLink CMD.
    """

    def __init__(self, connection_string, sleep=5, baud=9600):
        """Default Rover builder."""

        self._vehicle = initialize_vehicle(connection_string, baud)
        self._rest_time = sleep


    @property
    def vehicle(self):
        """Getter for Rover instance vehicle.

        Args:
            None

        Returns:
            A Vehicle instance representing the Rover vehicle.
        """

        return self._vehicle


    @vehicle.setter
    def vehicle(self, connection_string, baud=9600):
        """Setter for the Rover instance vehicle.

        Args:
            connection_string = A string representing the connection medium to
            the board.
            baud = An int representing the connection baud rate.

        Returns:
            None
        """

        self._vehicle = initialize_vehicle(connection_string, baud)


    @property
    def rest_time(self):
        """Getter for Rover instance rest_time.

        Args:
            None

        Returns:
            An int representing the vehicle rest time.
        """

        return self._rest_time


    @rest_time.setter
    def rest_time(self, sleep):
        """Setter for the Rover instance rest_time.

        Args:
            sleep = An int representing the vehicle rest time.

        Returns:
            None
        """

        self._rest_time = sleep


    def set_armed(self):
        """Enable rover armed mode.

        Args:
            None

        Returns:
            None
        """

        if not self._vehicle.armed:
            self._vehicle.armed = True


    def channel_override(self, yaw, speed):
        """Send RC override commands to the rover.

        Args:
            yaw = An int representing the yaw angle, between 1000 and 2000.
            speed = An int represneting the throttle, between 1000 and 2000.

        Returns:
            None
        """

        steering = min(max(1500 + yaw, 1000), 2000)
        throttle = min(max(1500 + speed, 1000), 2000)

        self._vehicle.channels.overrides = {'1':steering, '3':throttle}


    def mav_cmd_nav_set_yaw_speed(self, yaw, speed):
        """Send yaw angle and speed to vehicle via mavlink_cmd navigation.

        Documentation and MAVLINK CMD / ref: github:
        /mavlink/mavlink/blob/master/message_definitions/v1.0/common.xml#L531

        Args:
            yaw: A float representing the yaw angle in centidegrees.
            speed: A float between 0..1 representing the normalized yaw speed.

        Returns:
            None
        """

        msg = self.vehicle.message_factory.command_long_encode(
            0, # target_system
            0, # target_component
            213, # command id
            0, # confirmation
            yaw, # yaw angle (centideg)
            speed, # normalized 0 .. 1
            0, # unused
            0, # unused
            0, # unused
            0, # unused
            0) #unused

        self.vehicle.send_mavlink(msg)


    def change_rover_mode(self, mode):
        """Changes the current Rover navigation mode.

        Args:
            mode = A string representing the mode to change to. Possible values:
            AUTO, GUIDED, RETURN_TO_LAUNCH.

        Returns:
            None
        """

        if mode not in ['MANUAL', 'AUTO', 'GUIDED', 'RETURN_TO_LAUNCH']:
            logging.error("unknown mode %s, leaving mode unchanged.", str(mode))

        else:
            logging.info("current mode: %s, switching to %s", self.vehicle.mode,
                         mode)

            self.vehicle.mode = dronekit.VehicleMode(mode)

            time.sleep(self.rest_time)

            logging.info("current mode: %s", self.vehicle.mode)
