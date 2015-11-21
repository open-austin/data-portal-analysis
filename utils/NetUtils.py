# This file is part of Open Austin's Data Portal Analysis project.
# For more information see README.md in the project's root directory.

import requests
import logging

class ViewRequestHandler:
    def __init__(self):
        self._request_url = "http://data.austintexas.gov/views/"

    def get_view(self, socrata_id):
        request_url = self._request_url + socrata_id + '.json'
        try:
            result = requests.get(request_url)
        except:
            logging.critical("Can't get data from %s" % request_url)
        if 'error' in result.json().keys():
            logging.critical("Error getting data from %s message: %s"
                             % (request_url, result.json()['message']))
            return "error"

        logging.info("Got data from %s" % request_url)
        return result.json()
