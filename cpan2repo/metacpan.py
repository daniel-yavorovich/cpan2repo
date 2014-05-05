# -*- coding: utf-8 -*-
import requests


def get_release_info(cpan_name):
    """
    Get release info by
    module or distribution name
    """

    # Probably get info at release
    req_url = "http://api.metacpan.org/release/{cpan_name}".format(cpan_name=cpan_name).replace("::", "-")
    api_response = requests.get(req_url).json()

    if api_response.get("name"):
        return api_response

    req_url = "http://api.metacpan.org/module/{cpan_name}".format(cpan_name=cpan_name)
    api_response = requests.get(req_url).json()

    if api_response.get("distribution"):
        return get_release_info(api_response.get("distribution"))

    return {}
