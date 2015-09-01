"""
Handles making requests to the IndicoApi Server
"""

import json, requests

from indicoio.utils.errors import IndicoError, DataStructureException
from indicoio import JSON_HEADERS
from indicoio import config

def api_handler(arg, cloud, api, url_params=None, **kwargs):
    """
    Sends finalized request data to ML server and receives response.
    """

    data = {'data': arg}
    data.update(**kwargs)
    json_data = json.dumps(data)
    cloud = cloud or config.cloud
    host = "%s.indico.domains" % cloud if cloud else config.PUBLIC_API_HOST

    url = create_url(host, api, dict(kwargs, **url_params))
    response = requests.post(url, data=json_data, headers=JSON_HEADERS)

    if response.status_code == 503 and cloud != None:
        raise IndicoError("Private cloud '%s' does not include api '%s'" % (cloud, api))

    json_results = response.json()
    results = json_results.get('results', False)
    if results is False:
        error = json_results.get('error')
        raise IndicoError(error)
    return results


def create_url(host, api, url_params):
    api_key = url_params.get("api_key") or config.api_key
    is_batch = url_params.get("batch")
    apis = url_params.get("apis")
    version = url_params.get("version") or url_params.get("v")

    host_url_seg = config.url_protocol + "//%s" % host
    api_url_seg = "/%s" % api
    batch_url_seg = "/batch" if is_batch else ""
    key_url_seg = "?key=%s" % api_key
    multi_url_seg = "&apis=%s" % ",".join(apis) if apis else ""
    version_seg = ("&version=%s" % str(version)) if version else ""

    return host_url_seg + api_url_seg + batch_url_seg + key_url_seg \
            + multi_url_seg + version_seg
