import os

from indicoio import config

def test_batch_set_url_root_as_env_var():
    test_data = ['clearly an english sentence']
    old_private_cloud_url = os.environ.get("INDICO_PRIVATE_CLOUD_URL")
    os.environ["INDICO_PRIVATE_CLOUD_URL"] = "http://not.a.real.url/"

    assert config.get_api_root() == "http://not.a.real.url/"

    if old_private_cloud_url:
        os.environ["INDICO_PRIVATE_CLOUD_URL"] = old_private_cloud_url
    else:
        del(os.environ["INDICO_PRIVATE_CLOUD_URL"])
