"""
Module supporting the Camera class, responsible for taking snapshots.

class Camera: contains the builder and the main capture function.

"""

import os
import cv2

class Camera:
    """Class responsible for taking frames captures from webcam.

    This class initiates a Camera object and then invoke the main method
    called capture. Directly capture frames from the existing webcam.
    Relies on cv2 from frames capture and save.

    Attributes:
        device = An integer indicating the webcam device to use.
        path = A string indicating the path where frames are saved.
    """

    def __init__(self, path='./', device=0):
        """Init Camera with device nbr and path."""

        self._path = path
        self._device = device


    @property
    def path(self):
        """Getter for Camera instance path.

        Args:
            None

        Returns:
            A string representing the path where frames are saved.
        """

        return self._path


    @path.setter
    def path(self, path):
        """Setter for Camera instance path.

        Args:
            path: A string representing the new path.

        Returns:
            None
        """

        self._path = path


    @property
    def device(self):
        """Getter for Camera instance device.

        Args:
            None

        Returns:
            An int representing the webcam device.
        """

        return self._device


    @device.setter
    def device(self, device):
        """Setter for Camera instance device.

        Args:
            path: An int representing the new device.

        Returns:
            None
        """

        self._device = device


    def capture(self):
        """Capture frames from webcam.

        Starts the existing camera bound to the computer and starts
        taking snapshots, or frames. Relies on the cv2 library call
        for snapshots. Takes snapshots and saves them under self.path.

        Args:
            None

        Returns:
            None
        """

        cap = cv2.VideoCapture(self.device)
        _, frm = cap.read()

        cv2.imwrite(os.path.join(self.path, "frame.jpg"), frm)
        cap.release()
