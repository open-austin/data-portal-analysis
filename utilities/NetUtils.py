# This file is part of Open Austin's Data Portal Analysis project.
# For more information see README.md in the project's root directory.

import requests
import logging

logging.getLogger()

class SocIdGetter:
    def __init__(self):
        self._views_url = "https://data.austintexas.gov/views"
        self._migrations_api = "https://data.austintexas.gov/api/migrations/"
        self._view_metadata = self.get_all_view_ids()
        self._dataset_ids = self.filter_view_ids(self._view_metadata)

    def get_all_view_ids(self):
        req = requests.get(self._views_url)
        views_response_json = req.json()
        view_metadata = []
        for v in views_response_json:
            try:
                display_type = v['displayType']
            except(KeyError): # if v represents a data_lens page, we ignore it
                continue
            soc_id = v['id']
            view_type = v['viewType']
            display_type = v['displayType']
            item = [soc_id, view_type, display_type] # these attributes are used to filter out stuff we don't want
            view_metadata.append(item)
        return view_metadata    

    def filter_view_ids(self, view_metadata):
        dataset_ids = []
        for v in view_metadata:
            if v[1] == "tabular":
                if v[2] == "table":
                    dataset_ids.append(v)
                else:
                    continue
            else:
                continue
        return dataset_ids

    def filter_table_ids(self, dataset_ids):
        soc_ids = [] # these will be the "new back end" ids of primary data assets (not derived views, etc)
        for r in dataset_ids:
            soc_id = r[0]
            url = self._migrations_api + soc_id
            req = requests.get(url)
            response_json = req.json()
            try:
                i = response_json['nbeId']
            except(KeyError):
                continue
            soc_ids.append(i)
        return soc_ids
        
class ViewRequestHandler:
    def __init__(self):
        self._request_url = "http://data.austintexas.gov/views/"

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
        return result.json()
