import requests

from indicoio.utils.api import api_handler
from indicoio.utils.image import image_preprocess
import indicoio.config as config

def content_filtering(image, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given a grayscale input image, returns how obcene the image is.
    Input should be in a list of list format.

    Example usage:

    .. code-block:: python

       >>> from indicoio import content_filtering
       >>> import numpy as np
       >>> face = np.zeros((48,48)).tolist()
       >>> res = content_filtering(face)
       >>> res
	   .056

    :param image: The image to be analyzed.
    :type image: list of lists
    :rtype: float of nsfwness
    """
    image = image_preprocess(image, batch=batch, min_axis=128)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(image, cloud=cloud, api="contentfiltering", url_params=url_params, **kwargs)
