import json

import requests
import numpy as np

from indicoio import JSON_HEADERS

def facial_features(image):
    """
    Given an grayscale input image of a face, returns a 48 dimensional feature vector explaining that face.
    Useful as a form of feature engineering for face oriented tasks.
    Input should be in a list of list format, resizing will be attempted internally but for best 
    performance, images should be already sized at 48x48 pixels.

    Example usage:

    .. code-block:: python

       >>> from indicoio import facial_features
       >>> import numpy as np
       >>> face = np.zeros((48,48)).tolist()
       >>> features = facial_features(face)
       >>> len(features)
       48

    :param image: The image to be analyzed.
    :type image: list of lists
    :rtype: List containing feature responses
    """
    
    data_dict = json.dumps({"face": image})
    response = requests.post("http://api.indico.io/facialfeatures", data=data_dict, headers=JSON_HEADERS)
    response_dict = json.loads(response.content)
    return response_dict['response']
