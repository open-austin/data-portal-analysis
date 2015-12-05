import json
import csv
import datetime
import logging

logging.getLogger()


class DatasetAnalyzer:
    def __init__(self):
        """class DatasetAnalyzer()
        Analyzes a list of datasets and creates a CSV file with the results.
        """
        self._datasets = []

        # dataset_headers = ["id", "soc_resource_id", "name", "dept",
        #                    "snapshot_date_time"]
        # column_headers = ["col_position", "col_name", "col_field_name",
        #                   "soc_id", "soc_table_column_id",
        #                   "soc_data_type_name", "soc_render_type_name",
        #                   "num_null", "num_not_null", "ex_value"]
        self._generated_headers = ["is_current", "report_creation_time"]
#        self._headers = dataset_headers + column_headers + generated_headers

        cur_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        self._creation_time = cur_time
        self._rows = []

    def add_dataset(self, dataset):
        if dataset['id'] in self._datasets:
            logging.warn("Dataset already analyzed: %s" % dataset['id'])
            return
        else:
            self._rows.extend(self._analyze_dataset(dataset))
            self._datasets.append(dataset['id'])

    def _analyze_dataset(self, dataset):
        """Analyze a dataset (dict) and return a list of rows.
        """
        logging.debug("Analyzing %s: %s"
                      % (dataset['id'], dataset['name']))

        rows = []
        dataset_info = self._get_dataset_info(dataset)
        if 'columns' not in dataset.keys():
            logging.warn("No columns in %s" % dataset['id'])
            raise KeyError("No Columns")
        for col in dataset['columns']:
            current_row = []
            current_row.extend(dataset_info)
            current_row.append(u"IS_CURRENT")         # placeholder
            current_row.append(self._creation_time)
            encoded_row = []      # csv module doesn't like unicode
            for item in current_row:
                if isinstance(item, unicode):
                    item = item.encode('utf-8')
                encoded_row.append(item)

            rows.append(encoded_row)
        return rows

    def _analyze_all(self):
        """Run the analyzer on all datasets and return the results.
        """
        results = []
        for item in self._datasets:
            try:
                analyzed_content = self._analyze_dataset(item)
            except(KeyError):
                continue
            for row in analyzed_content:
                results.append(row)
        return results

    def _get_dataset_info(self, dataset):
        """Returns dataset info (common to all columns) as a list.
        """
        dataset_id = dataset['id']
        dataset_name = dataset['name']
        dataset_time = self._get_date_time(dataset)
        try:
            custom = dataset['metadata']['custom_fields']
            dataset_dpt = custom['Additional Information']['Department']
        except:
            dataset_dpt = "null"
            logging.debug("No department information for dataset %s"
                          % dataset_id)

        return [dataset_id, dataset_name, dataset_dpt, dataset_time]

    def _get_column_info(self, col):
        """Returns information about the given column as a list.
        """
        current_row = []
        current_row.append(col['position'])
        current_row.append(col['name'])
        current_row.append(col['fieldName'])
        current_row.append(col['id'])
        current_row.append(col['tableColumnId'])
        current_row.append(col['dataTypeName'])
        current_row.append(col['renderTypeName'])
        return current_row

    def _get_date_time(self, dataset):
        """This function fills the snapshot_date_time column.
        """
        try:
            date = dataset['snapshot_date_time']
        except(KeyError):
            logging.warn("snapshot_time not found for dataset %s"
                         % dataset['id'])
            date = "null"
        return date

    def get_headers(self):
        with open("utilities/headers.json") as headerfile:
            headerset = headerfile.read()
            headers = ['id']
            headers.extend(self._analyze_dataset(json.loads(headerset))[0][:-2])
            headers.extend(self._generated_headers)
            return headers

    def make_csv(self, filename=None):
        if filename is None:
            print(self.get_headers())            
            for number, row in enumerate(self._rows):
                print([number+1]+row)
            return
        with open(filename, "wb") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.get_headers())
            for number, row in enumerate(self._rows):
                writer.writerow([number+1]+row)
        return
