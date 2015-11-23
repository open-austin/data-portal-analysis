# This file is part of Open Austin's Data Portal Analysis project.
# For more information see README.md in the project's root directory.

import requests
import logging
import datetime

logging.getLogger()


class SocIdGetter:
    def __init__(self):
        self._views_url = "http://data.austintexas.gov/api/search/views.json"
        self._migrations_api = "http://data.austintexas.gov/api/migrations/"
        self._view_metadata = self.get_all_view_ids()
        self._tabular_ids = self.filter_view_ids(self._view_metadata)
        self.fourby_list = self.filter_tabular_ids(self._tabular_ids)

    def get_all_view_ids(self):
        req = requests.get(self._views_url)
        views_response_json = req.json()
        view_metadata = []
        for view in views_response_json['results']:
            try:
                display_type = view['view']['displayType']
            except(KeyError): # this means the the view represents a data_lens page, so we ignore it
                continue
            soc_id = view['view']['id']
            view_type = view['view']['viewType']
            display_type = view['view']['displayType']
            item = [soc_id, view_type, display_type] # these attributes are used later on to filter out stuff we don't want
            view_metadata.append(item)
        return view_metadata    

    def filter_view_ids(self, view_metadata):
        tabular_ids = []
        for i in view_metadata:
            if i[1] == "tabular":
                if i[2] == "table":
                    tabular_ids.append(i[0])
                else:
                    continue
            else:
                continue
        return tabular_ids

    def filter_tabular_ids(self, tabular_ids):
        fourby_list = [] # these will be the "new back end" ids of primary data assets
        for i in tabular_ids:
            url = self._migrations_api + i
            req = requests.get(url)
            response_json = req.json()
            try:
                fourby_item = response_json['nbeId']
            except(KeyError):
                logging.info("%s is not a primary data asset."
                             % i)
                print url # added temporarily for debugging
                continue
            else:
                fourby_list.append(fourby_item)
        return fourby_list
        
class ViewRequestHandler:
    def __init__(self):
        self._request_url = "http://data.austintexas.gov/api/views/"

    def get_view(self, socrata_id):
        request_url = self._request_url + socrata_id + '.json'
        try:
            result = requests.get(request_url)
        except:
            logging.critical("Can't get data from %s" % request_url)
            return "null"
        if 'error' in result.json().keys():
            logging.critical("Error getting data from %s message: %s"
                             % (request_url, result.json()['message']))
            return "null"
        logging.info("Got data from %s" % request_url)

        dataset = result.json()
        cur_time = datetime.datetime.now().replace(microsecond=0)
        dataset['snapshot_time'] = cur_time.isoformat()

        return dataset
