"""This module includes the darknet python wrapper. It includes several
helper class and the darknet wrapper itself.

function sample: get a sample from a probability distribution.

function c_array: returns a c-type array from a list of values.

class BOX: C-style struct representing a x-y box.

class DETECTION: C-style struct representing a detection item.

class IMAGES: C-style struct representing an image.

class METADATA: C-style struct representing model metadata.

class pydarknet: Darknet wrapper for python class.
"""

#pylint: disable=too-few-public-methods


import ctypes
import random


def sample(probs):
    """Get a sample from a probability distribution.

    Args:
        probs: A list of probabilities.

    Return:
        A sample i from the probability distribution described by probs.
    """

    total = sum(probs)
    probs = [prb/total for prb in probs]

    randval = random.uniform(0, 1)

    for i, _val in enumerate(probs):

        randval = randval - probs[i]

        if randval <= 0:
            return i

    return len(probs)-1


def c_array(ctype, values):
    """Returns a C-type array from list of values.

    Args:
        ctype: A c-type type.
        values: A list of values for the c-type array.

    Returns:
        A c-type array filled with values 'values'.
    """

    arr = (ctype*len(values))()
    arr[:] = values
    return arr


class BOX(ctypes.Structure):
    """C-style struct representing a x-y box."""

    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("w", ctypes.c_float),
                ("h", ctypes.c_float)]


class DETECTION(ctypes.Structure):
    """C-style struct representing a detection item."""

    _fields_ = [("bbox", BOX),
                ("classes", ctypes.c_int),
                ("prob", ctypes.POINTER(ctypes.c_float)),
                ("mask", ctypes.POINTER(ctypes.c_float)),
                ("objectness", ctypes.c_float),
                ("sort_class", ctypes.c_int)]


class IMAGE(ctypes.Structure):
    """C-style struct representing an image."""

    _fields_ = [("w", ctypes.c_int),
                ("h", ctypes.c_int),
                ("c", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.c_float))]


class METADATA(ctypes.Structure):
    """C-style struct representing model metadata."""

    _fields_ = [("classes", ctypes.c_int),
                ("names", ctypes.POINTER(ctypes.c_char_p))]


def init_lib(libpath):
    """Initialize the library.

    Args:
        libpath = A string representing the library path.

    Returns:
        An initialized library object.
    """

    library = ctypes.CDLL(libpath, ctypes.RTLD_GLOBAL)

    library.network_width.argtypes = [ctypes.c_void_p]
    library.network_width.restype = ctypes.c_int
    library.network_height.argtypes = [ctypes.c_void_p]
    library.network_height.restype = ctypes.c_int

    return library


class Pydarknet():
    """Python wrapper class for C backend Darknet.

    Attributes:
        library = The darknet library.
    """

    def __init__(self, libpath):
        """Pydarknet default builder."""

        self.library = init_lib(libpath)


    def init_predict(self):
        """Init and return a predict object."""

        predict = self.library.network_predict
        predict.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float)]
        predict.restype = ctypes.POINTER(ctypes.c_float)

        return predict


    def init_set_gpu(self):
        """Init and return a set_gpu object."""

        set_gpu = self.library.cuda_set_device
        set_gpu.argtypes = [ctypes.c_int]

        return set_gpu


    def init_make_image(self):
        """Init and return a make_image object."""

        make_image = self.library.make_image
        make_image.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        make_image.restype = IMAGE

        return make_image


    def init_get_network_boxes(self):
        """Init and return a get_network_boxes object."""

        get_network_boxes = self.library.get_network_boxes
        get_network_boxes.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_float,
                                      ctypes.c_float, ctypes.POINTER(ctypes.c_int),
                                      ctypes.c_int, ctypes.POINTER(ctypes.c_int)]

        get_network_boxes.restype = ctypes.POINTER(DETECTION)

        return get_network_boxes


    def init_make_network_boxes(self):
        """Init and return a make_network_boxes object."""

        make_network_boxes = self.library.make_network_boxes
        make_network_boxes.argtypes = [ctypes.c_void_p]
        make_network_boxes.restype = ctypes.POINTER(DETECTION)

        return make_network_boxes


    def init_free_detections(self):
        """Init and return a free_detections object."""

        free_detections = self.library.free_detections
        free_detections.argtypes = [ctypes.POINTER(DETECTION), ctypes.c_int]

        return free_detections


    def init_free_ptrs(self):
        """Init and return a free_ptrs object."""

        free_ptrs = self.library.free_ptrs
        free_ptrs.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int]

        return free_ptrs


    def init_network_predict(self):
        """Init and return a network_predit object."""

        network_predict = self.library.network_predict
        network_predict.argtypes = [ctypes.c_void_p,
                                    ctypes.POINTER(ctypes.c_float)]

        return network_predict


    def init_reset_rnn(self):
        """Init and return a reset_rnn object."""

        reset_rnn = self.library.reset_rnn
        reset_rnn.argtypes = [ctypes.c_void_p]

        return reset_rnn


    def init_load_net(self):
        """Init and return a load_net object."""

        load_net = self.library.load_network
        load_net.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        load_net.restype = ctypes.c_void_p

        return load_net


    def init_do_nms_obj(self):
        """Init and return a do_nms_obj object."""

        do_nms_obj = self.library.do_nms_obj
        do_nms_obj.argtypes = [ctypes.POINTER(DETECTION), ctypes.c_int,
                               ctypes.c_int, ctypes.c_float]

        return do_nms_obj


    def init_do_nms_sort(self):
        """Init and return a do_nms_sort object."""

        do_nms_sort = self.library.do_nms_sort
        do_nms_sort.argtypes = [ctypes.POINTER(DETECTION), ctypes.c_int,
                                ctypes.c_int, ctypes.c_float]

        return do_nms_sort


    def init_free_image(self):
        """Init and return a free_image object."""

        free_image = self.library.free_image
        free_image.argtypes = [IMAGE]

        return free_image


    def init_letterbox_image(self):
        """Init and return a letterbox_image object."""

        letterbox_image = self.library.letterbox_image
        letterbox_image.argtypes = [IMAGE, ctypes.c_int, ctypes.c_int]
        letterbox_image.restype = IMAGE

        return letterbox_image


    def init_load_meta(self):
        """Init and return a load_meta object."""

        load_meta = self.library.get_metadata
        self.library.get_metadata.argtypes = [ctypes.c_char_p]
        self.library.get_metadata.restype = METADATA

        return load_meta


    def init_load_image(self):
        """Init and return a load_image object."""

        load_image = self.library.load_image_color
        load_image.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        load_image.restype = IMAGE

        return load_image


    def init_rgbgr_image(self):
        """Init and return a rgbgr_image object."""

        rgbgr_image = self.library.rgbgr_image
        rgbgr_image.argtypes = [IMAGE]

        return rgbgr_image


    def init_predict_image(self):
        """Init and return a predict_image object."""

        predict_image = self.library.network_predict_image
        predict_image.argtypes = [ctypes.c_void_p, IMAGE]
        predict_image.restype = ctypes.POINTER(ctypes.c_float)

        return predict_image


    def classify(self, net, meta, img):
        """Classify objects in an image.

        Args:
            net: A net object representing the network to use.
            meta: A meta object representing the model metadata.
            img: An image object representing the image to classify.

        Returns:
            A list of detected objects as a result.
        """

        predict_image = self.init_predict_image()
        out = predict_image(net, img)
        res = []
        for i in range(meta.classes):
            res.append((meta.names[i], out[i]))
        res = sorted(res, key=lambda x: -x[1])
        return res


    def detect(self, model, thresh=.5, hier_thresh=.5, nms=.45): #pylint: disable=too-many-locals
        """Detect objects in an image.

        Args:
            net: A net object representing the network to use.
            meta: A meta object representing the model metadata.
            image: An image object representing the image to classify.
            thresh: An float representing the detection threshold.
            hier_thresh: A float representing the detection threshold.
            nms: A float representing a model parameter value.

        Returns:
            A list of detected objects bounding boxes as a result.
        """

        net, meta, image = model

        img = self.init_load_image()(image, 0, 0)

        num = ctypes.c_int(0)
        pnum = ctypes.pointer(num)

        self.init_predict()
        self.init_set_gpu()
        self.init_make_image()

        self.init_predict_image()(net, img)

        dets = self.init_get_network_boxes()(net, img.w, img.h, thresh,
                                             hier_thresh, None, 0, pnum)

        num = pnum[0]
        if nms:
            self.init_do_nms_obj()(dets, num, meta.classes, nms)

        res = []
        for j in range(num):
            for i in range(meta.classes):
                if dets[j].prob[i] > 0:
                    bound = dets[j].bbox
                    res.append((meta.names[i], dets[j].prob[i],
                                (bound.x, bound.y, bound.w, bound.h)))

        res = sorted(res, key=lambda x: -x[1])

        self.init_free_image()(img)

        self.init_free_detections()(dets, num)

        return res
