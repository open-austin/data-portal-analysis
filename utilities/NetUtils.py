# This file is part of Open Austin's Data Portal Analysis project.
# For more information see README.md in the project's root directory.

import requests
import logging
import datetime

logging.getLogger()


class SocIdGetter:
    def __init__(self):
        self._views_url = "http://data.austintexas.gov/views"
        self._migrations_api = "http://data.austintexas.gov/api/migrations/"
        self._view_metadata = self.get_all_view_ids()
        self.soc_ids = self.filter_view_ids(self._view_metadata)

    def get_all_view_ids(self):
        req = requests.get(self._views_url)
        views_response_json = req.json()
        view_metadata = []
        for view in views_response_json:
            try:
                display_type = view['displayType']
            except(KeyError): # if view represents a data_lens page, we ignore it
                continue
            soc_id = view['id']
            view_type = view['viewType']
            display_type = view['displayType']
            item = [soc_id, view_type, display_type] # these attributes are used to filter out stuff we don't want
            view_metadata.append(item)
        return view_metadata    

    def filter_view_ids(self, view_metadata):
        dataset_ids = []
        for data_list in view_metadata:
            if data_list[1] == "tabular":
                if data_list[2] == "table":
                    dataset_ids.append(data_list[0])
                else:
                    continue
            else:
                continue
        return dataset_ids

    def filter_table_ids(self, dataset_ids):
        fourby_list = [] # these will be the "new back end" ids of primary data assets (not derived views, etc)
        for set_id in dataset_ids:
            url = self._migrations_api + set_id
            req = requests.get(url)
            response_json = req.json()
            try:
                new_id = response_json['nbeId']
            except(KeyError):
                logging.info("%s is not a primary data asset."
                             % set_id)
                continue
            else:
                soc_ids.append(new_id)
        return fourby_list
        
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

        dataset = result.json()
        cur_time = datetime.datetime.now().replace(microsecond=0)
        dataset['snapshot_time'] = cur_time.isoformat()

        return dataset
