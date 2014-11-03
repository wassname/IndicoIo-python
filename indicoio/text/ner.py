from indicoio.utils import api_handler

def named_entities(api_root, text):
    """
    Given input text, returns a mapping from named entities to 
    named entity categories.

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = 'On Monday, president Barack Obama will be...'
       >>> indicoio.named_entities(text)
       >>> "{'Monday': 'Time', 'Barack Obama': 'Person'}"

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Dictionary of named entity, category pairs
    """
    
    return api_handler(text, api_root + "ner")
