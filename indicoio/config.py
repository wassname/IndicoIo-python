import os
from StringIO import StringIO

import ConfigParser

class Settings(ConfigParser.ConfigParser):

    def __init__(self, *args, **kwargs):
        """
        files: filepaths or open file objects
        """
        self.files = kwargs.pop('files')

        ConfigParser.ConfigParser.__init__(self, *args, **kwargs)

        for fd in self.files:
            try:
                self.readfp(fd)
            except AttributeError:
                self.read(fd)

        self.auth_settings = self.get_section('auth')
        self.private_cloud_settings = self.get_section('private_cloud')

    def get_section(self, section):
        """
        Retrieve a ConfigParser section as a dictionary, default to {}
        """
        try:
            return dict(self.items(section))
        except ConfigParser.NoSectionError:
            return {}

    def cloud(self):
        return (
            os.getenv("INDICO_CLOUD") or
            self.private_cloud_settings.get('cloud') or
            None
        )

    def api_key(self):
        return (
            os.getenv("INDICO_API_KEY") or
            self.auth_settings.get('api_key') or
            None
        )

TEXT_APIS = [
    'text_tags',
    'political',
    'sentiment',
    'language',
    'sentiment_hq',
    'keywords',
    'named_entities',
    'twitter_engagement'
]

IMAGE_APIS = [
    'fer',
    'facial_features',
    'image_features',
    'image_recognition',
    'content_filtering'
]

OTHER_APIS = [
    "analyze_text",
    "analyze_image",
    "intersections"
]

API_NAMES = IMAGE_APIS + TEXT_APIS + OTHER_APIS

SETTINGS = Settings(files=[
    os.path.expanduser("~/.indicorc"),
    os.path.join(os.getcwd(), '.indicorc')
])

api_key = SETTINGS.api_key()
cloud = SETTINGS.cloud()
PUBLIC_API_HOST = 'apiv2.indico.io'
url_protocol = "https:"
