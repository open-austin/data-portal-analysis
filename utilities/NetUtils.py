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


    def _download_views(self):
        """This function downloads views.json in chunks and informs the user of
        progress every 100 chunks."""
        localfile = 'views.json'
        req = requests.get(self._views_url, stream=True)
        chunknum = 0
        logging.info("Downloading {0}".format(self._views_url))
        with open(localfile, 'wb') as local_f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    if(chunknum % 100 == 0):
                        logging.info("Got chunk {0} of {1}.".format(chunknum, localfile))
                    local_f.write(chunk)
                    chunknum += 1
            logging.info("views.json was downloaded in {0} chunks".format(chunknum))
        with open(localfile) as view_json:
            json_str = view_json.read()
            views_dict = json.loads(json_str)
        return views_dict


    def get_ids(self, viewfile=False):
        """Fetches views from Socrata, returns a list of 4x4 socrata ids."""
        if viewfile:
            with open('views.json') as viewjson:
                views_dict = json.loads(viewjson.read())
        else:
            views_dict = self._download_views()

        id_list = []
        for view in views_dict['results']:
            try:
                display_type = view['view']['displayType']
            except(KeyError):
                # this means the the view represents a data_lens page,
                # so we ignore it
                continue
            if view['view']['viewType'] == "tabular":
                if view['view']['displayType'] == "table":
                    id_list.append(view['view']['id'])

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
