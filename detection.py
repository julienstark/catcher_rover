"""
Module supporting the Detection class, responsible for running Darknet object
detection and returning bounding boxes coordinates.

class Detection: contains the builder the main detector functions.
"""

import pydarknet #pylint: disable=import-error
import cv2 #pylint: disable=import-error

import utils


def initialize_detector(config, weights, data):
    """Initialize the detector model.

    Args:
        config: A string representing the path of the Darknet cfg file.
        weights: A string representing the path of the Darknet weights file.
        data: A string representing the path of the Darknet data file.

    Returns:
        A detector object representing the darknet model.
    """

    suppress_output = utils.SuppressStdOutput()

    with suppress_output:
        net = pydarknet.Detector(bytes(config, encoding="utf-8"),
                                 bytes(weights, encoding="utf-8"),
                                 0,
                                 bytes(data, encoding="utf-8"))

    return net


def initialize_image(img):
    """Initialize the Darknet image.

    Args:
        img: A string representing the path of an image.

    Returns:
        An instance of a Darknet Image.
    """

    image = pydarknet.Image(cv2.imread(img))

    return image


class Detection():
    """Class responsible for running object detection on an image.

    Attributes:
        detector: a Detector object representing the Darknet model.
        image: an Image object representing the image to be processed.
    """

    def __init__(self, config, weights, data, img):
        """Initiates the builder for Detection"""

        self._detector = initialize_detector(config, weights, data)
        self._image = initialize_image(img)


    @property
    def detector(self):
        """Getter for Detection instance detector.

        Args:
            None

        Returns:
            A detector object representing the current Darknet model.
        """

        return self._detector


    @detector.setter
    def detector(self, config, weights, data):
        """Setter for Detection instance detector.

        Args:
            config: A string representing the path of the Darknet cfg file.
            weights: A string representing the path of the Darknet weights file.
            data: A string representing the path of the Darknet data file.

        Returns:
            None
        """

        self._detector = initialize_detector(config, weights, data)


    @property
    def image(self):
        """Getter for Detection instance image.

        Args:
            None

        Returns:
            An Image object representing an image.
        """

        return self._image


    @image.setter
    def image(self, img):
        """Setter for Detection instance image.

        Args:
            img: A string representing the path of an image.

        Returns:
            None
        """

        self._image = initialize_image(img)


    def get_coordinates(self, label):
        """Get a list of coordinates for bounding boxes corresponding to label.

        Args:
            label: A string representing the label to detect.

        Returns:
            A list with tupes including the x, y, width and height values of
            the detected boundig boxes for the label.
        """

        bounding_boxes = []
        results = self.detector.detect(self.image)

        for objects in results:
            if objects[0].decode('utf-8') == label:
                bounding_boxes.append(objects[2])

        return bounding_boxes
