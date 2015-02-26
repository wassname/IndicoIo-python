import os

import ConfigParser

settings = ConfigParser.ConfigParser()

settings_paths = [
    os.path.expanduser("~/.indicorc"),
    os.path.join(os.getcwd(), '.indicorc')
]

settings.read(settings_paths)

def get_section(parser, section):
    try:
        return dict(parser.items(section))
    except ConfigParser.NoSectionError:
        return {}

auth_settings = get_section(settings, 'auth')
private_cloud_settings = get_section(settings, 'private_cloud')

api_root = (
    os.getenv("INDICO_PRIVATE_CLOUD_URL") or 
    private_cloud_settings.get('url_root') or 
    "http://apiv1.indico.io/"
)

auth = (auth_settings.get('username'), auth_settings.get('password'))
