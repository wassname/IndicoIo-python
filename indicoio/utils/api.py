"""
Handles making requests to the IndicoApi Server
"""

import json, requests

from indicoio.utils.errors import IndicoError, DataStructureException
from indicoio import JSON_HEADERS
from indicoio import config

def api_handler(arg, cloud, api, url_params = {"batch":False, "api_key":None}, **kwargs):
    data = {'data': arg}
    data.update(**kwargs)
    json_data = json.dumps(data)
    if not cloud:
        cloud=config.cloud

    if cloud:
        host = "%s.indico.domains" % cloud

    else:
        # default to indico public cloud
        host = config.PUBLIC_API_HOST

        # error message for public cloud
        if api == 'sentimenthq':
            raise IndicoError("The high quality sentiment API is currently in private beta.")

    url = config.url_protocol + "//%s/%s" % (host, api)
    url = url + "/batch" if url_params.get("batch", False) else url
    url += "?key=%s" % (url_params.get("api_key", None) or config.api_key)
    if "apis" in url_params:
        url += "&apis=%s" % ",".join(url_params["apis"])

    response = requests.post(url, data=json_data, headers=JSON_HEADERS)
    if response.status_code == 503 and cloud != None:
        raise IndicoError("Private cloud '%s' does not include api '%s'" % (cloud, api))

    json_results = response.json()
    results = json_results.get('results', False)
    if results is False:
        error = json_results.get('error')
        raise IndicoError(error)
    return results
