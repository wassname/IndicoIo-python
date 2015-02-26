import os

def get_api_root():
    return os.environ.get("INDICO_PRIVATE_CLOUD_URL") or "http://apiv1.indico.io/"
api_root = get_api_root()
