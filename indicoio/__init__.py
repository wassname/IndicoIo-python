from functools import partial
from utils import config

JSON_HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

Version, version, __version__, VERSION = ('0.4.5',) * 4

from text.sentiment import political, posneg
from text.sentiment import posneg as sentiment
from text.lang import language
from images.fer import fer
from images.features import facial_features
from images.features import image_features

political = partial(political, config.api_root)
posneg = partial(posneg, config.api_root)
sentiment = partial(sentiment, config.api_root)
posneg = partial(sentiment, config.api_root)
language = partial(language, config.api_root)
fer = partial(fer, config.api_root)
facial_features = partial(facial_features, config.api_root)
image_features = partial(image_features, config.api_root)
