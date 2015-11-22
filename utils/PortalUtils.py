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

        dataset_headers = ["id", "soc_resource_id", "dept",
                           "snapshot_date_time"]
        column_headers = ["name", "col_position", "col_name", "col_field_name",
                          "soc_id", "soc_table_column_id",
                          "soc_data_type_name", "soc_render_type_name",
                          "num_null", "num_not_null", "ex_value"]
        generated_headers = ["is_current", "report_creation_time"]
        self._headers = dataset_headers + column_headers + generated_headers

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
            current_row.extend(self._get_column_info(col))
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
        current_row.extend(self._get_cached_contents(col))
        return current_row

    def _get_cached_contents(self, col):
        """This function retrieves information from columns
        that have a section for cached contents.
        """
        return_list = []
        try:
            cached = col['cachedContents']
            return_list.append(cached['null'])
            return_list.append(cached['non_null'])
        except:
            logging.debug("No cachedContents found for column %s"
                          % col['fieldName'])
            return_list.extend(['null', 'null'])

        # The following code (for processing the 'top' field) needs work,
        # but first we need to decide how unexpected content should
        # be handled.
        try:
            top = col['cachedContents']['top']
            item = top[0]['item']
        except:
            return_list.append('null')
            return return_list

        if col['dataTypeName'] == 'url':
            try:
                item = item['url']
            except:
                logging.warn("""In top url for column %s: no associated url.
        Object: %s"""
                             % (col['fieldName'], repr(item)))
                item = 'null'

        if col['dataTypeName'] == 'location':
            try:
                item = item['human_address']
            except(KeyError):
                pass

        return_list.append(item)
        return return_list

    def _get_date_time(self, dataset):
        """This function fills the snapshot_date_time column.
        """
        try:
            date = dataset['snapshot_time']
        except(KeyError):
            logging.warn("snapshot_time not found for dataset %s"
                         % dataset['id'])
            date = "null"
        return date

    def make_csv(self, filename):
        if len(self._rows) == 0:
            raise Exception("Add datasets before calling make_csv")
        with open(filename, "wb") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self._headers)
            for number, row in enumerate(self._rows):
                writer.writerow([number+1]+row)
