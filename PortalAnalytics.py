import json
import csv
import sys


class DatasetAnalyzer():
    def __init__(self, json_filename, output_filename):
        """Initialize a Dataset Analyzer object.
        """
        self._outfile = output_filename

        with open(json_filename) as data_json:
            json_str = data_json.read()
            data_dict = json.loads(json_str)
        self._datasets = data_dict['datasets']  # This will need to change

        self._headers = ["id", "soc_resource_id", "dept", "name",
                         "col_position", "col_name", "col_field_name",
                         "soc_id", "soc_table_column_id",
                         "soc_data_type_name", "soc_render_type_name",
                         "num_null", "num_not_null", "ex_value",
                         "snapshot_date_time", "is_current"]

    def _analyze_dataset(self, dataset):
        """Analyze a dataset (dict) and return a list of rows.
        """
        # TODO find a cleaner way to deal with encoding issues
        rows = []
        dataset_id = dataset['id']
        dataset_name = dataset['name'].encode('utf-8')
        dataset_dpt = self._get_department(dataset)
        dataset_time = self._get_date_time(dataset)

        for col in dataset['columns']:
            current_row = []
            current_row += [dataset_id, dataset_dpt, dataset_name]
            current_row += [col['position']]
            current_row += [col['name'].encode('utf-8')]
            current_row += [col['fieldName'].encode('utf-8')]
            current_row += [col['id']]
            current_row += [col['tableColumnId']]
            current_row += [col['dataTypeName'].encode('utf-8')]
            current_row += [col['renderTypeName'].encode('utf-8')]
            current_row += [self._get_null_count(col)]
            current_row += [self._get_non_null_count(col)]
            current_row += [self._get_top(col)]
            current_row += [dataset_time]
            current_row += ["IS_CURRENT"]         # placeholder
            rows.append(current_row)

        return rows

    def _analyze_all(self):
        """Run the analyzer on all datasets and return the results.
        """
        results = []
        rows = []
        results.append(self._headers)
        for item in self._datasets:
            for row in self._analyze_dataset(item):
                rows.append(row)
        for number, row in enumerate(rows):
            results.append([number+1] + row)
        return results

    def _get_department(self, dataset):
        try:
            custom = dataset['metadata']['custom_fields']
            dpt = custom['Additional Information']['Department']
        except:
            # print dataset['name']
            dpt = "No Department Information"
        return dpt.encode('utf-8')

    def _get_null_count(self, col):
        try:
            total = col['cachedContents']['null']
        except:
            total = "null"
        return total

    def _get_non_null_count(self, col):
        try:
            total = col['cachedContents']['non_null']
        except:
            total = "null"
        return total

    def _get_top(self, col):
        """This gets the top item from cachedContents.
        Currently the item is returned as a python representation,
        which is less than ideal, but it works.

        """
        try:
            top = col['cachedContents']['top'][0]['item']
        except:
            top = "null"
        return repr(top)

    def _get_date_time(self, dataset):
        try:
            date = dataset['publicationDate']
        except:
            date = "null"
        return date

    def make_csv(self):
        with open(self._outfile, "wb") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            for row in self._analyze_all():
                writer.writerow(row)


if __name__ == "__main__":
    """USAGE: python PortalAnalytics.py <input file> <output file>
    """
    filename = "datasets.json"
    outfile = "out.csv"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]

    Analyzer = DatasetAnalyzer(filename, outfile)
    Analyzer.make_csv()
