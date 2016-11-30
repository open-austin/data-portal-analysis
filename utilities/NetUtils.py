# This file is part of Open Austin's Data Portal Analysis project.
# For more information see README.md in the project's root directory.

import requests
import logging
import datetime
import json

logging.getLogger()

class SocIdGetter(object):
    """class SocIdGetter()
    Fetches a collection of views from data.austintexas.gov, and populates a collection
    of view id's and types
    """
    def __init__(self, views_url, migrations_url):
        """Initializes a Socrata Id Getter.
        Retrieves view metadata from Socrata, and filters / retrieves tabular data
        for each view.
        """
        self._views_url = views_url
        self._migrations_api = migrations_url


    def get_ids(self, viewfile=False, limit=None):
        """Fetches views from Socrata, returns a list of 4x4 socrata ids."""
        catalog_url = "http://api.us.socrata.com/api/catalog/v1"
        if limit is None:
            response = requests.get(catalog_url + "?domains=data.austintexas.gov&only=datasets&limit=1")
            result_size = response.json()['resultSetSize']
        else:
            result_size = limit
        id_list = []
        for start_number in range(0, result_size, 500):
            response = requests.get(catalog_url + "?domains=data.austintexas.gov&only=datasets&limit=500&offset=" + str(start_number))
            for result in response.json()['results']:
                id_list.append(result['resource']['id'])
                
        migrated_ids = [self._migrate_id(obe_id) for obe_id in id_list]
        migrated_ids = [soc_id for soc_id in migrated_ids if soc_id is not None]
        return migrated_ids

    def _migrate_id(self, obe_id):
        """For each set of tabular data, fetch updated id from Socrata's
        migrations api.
        """
        url = self._migrations_api + obe_id
        req = requests.get(url)
        response_json = req.json()
        try:
            nbe_id = response_json['nbeId']
            return nbe_id
        except(KeyError):
            logging.info("{0} is not a primary data asset.".format(obe_id))
            return None


class ViewRequestHandler(object):
    """class ViewRequestHandler()
    Fetches view data given a Socrata id.
    """
    def __init__(self, view_api_url):
        """Initializes view request url."""
        self._request_url = view_api_url

    def get_view(self, socrata_id):
        """Fetches view data for a given socrata_id."""
        request_url = self._request_url + socrata_id + '.json'
        result = requests.get(request_url)
        if result.status_code is 404:
            logging.critical("404 response from {0}".format(request_url))
            return "null"
        if 'error' in result.json().keys():
            logging.critical("Error getting data from {0} message: {1}".format(request_url, result.json()['message']))
            return "null"
        logging.info("Got data from {0}".format(request_url))

        dataset = result.json()
        cur_time = datetime.datetime.now().replace(microsecond=0)
        dataset['snapshot_date_time'] = cur_time.isoformat()

        return dataset
