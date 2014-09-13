import requests
import json

from indicoio import JSON_HEADERS

def language(text):
    """
    Given input text, returns a probability distribution over 33 possible 
    languages of what language the text was written in.

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> possible = indicoio.language(text)
       >>> language = possible.keys()[np.argmax(possible.values())]
       >>> probability = np.max(possible.values())
       >>> 'Predicted %s with probability %.4f'%(language,probability)
       u'Predicted English with probability 0.8548'

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of language probability pairs
    """
    
    data_dict = json.dumps({'text': text})
    response = requests.post("http://api.indico.io/language", data=data_dict, headers=JSON_HEADERS)
    response_dict = response.json()
    if len(response_dict) < 2:
      raise ValueError(response_dict.values()[0])
    else:
      return response_dict