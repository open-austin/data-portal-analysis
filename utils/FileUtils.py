# This file is part of Open Austin's Data Portal Analysis project.
# For more information see README.md in the project's root directory.

import json
import datetime


class JsonFileReader:
    """ class JsonFileHandler(json_filename)
    Opens a JSON file and prepares datasets for analysis.
    """
    def __init__(self, json_filename):
        self._current_time = datetime.datetime.now()
        self._current_time.replace(microsecond=0).isoformat()
        dataset_dict = self._load_json(json_filename)
        self._datasets = self._multiset_handler(dataset_dict)

    def _load_json(self, json_filename):
        with open(json_filename) as data_json:
            json_str = data_json.read()
            data_dict = json.loads(json_str)
        return data_dict

    def _multiset_handler(self, data_dict):
        try:
            datasets = data_dict['datasets']
        except(KeyError):
            datasets = [data_dict]
        except:
            raise KeyError("No datasets found")

        for item in datasets:
            item['snapshot_time'] = self._current_time
        return datasets

    def get_all_datasets(self):
        """Return a list of dataset dicts.
        """
        return self._datasets
