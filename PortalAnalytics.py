import json
import csv

class DatasetAnalyzer():
    def __init__(self, json_filename, output_filename):
        """Initialize a Dataset Analyzer object.
        """
        self._outfile = output_filename

        with open(json_filename) as data_json:
            json_str = data_json.read()
            data_dict = json.loads(json_str)
        self._datasets = data_dict['datasets'] # This will need to change

        self._headers = ["id", "soc_resource_id", "dept", "name",
                         "col_position", "col_name", "col_field_name",
                         "soc_id", "soc_table_column_id",
                         "soc_data_type_name", "soc_render_type_name",
                         "num_null", "num_not_null", "ex_value",
                         "snapshot_date_time", "is_current"]

    def run(self):
        csv_info = []
        rows = []
        csv_info.append(self._headers)
        for item in self._datasets:
            for row in self._analyze_dataset(item):
                rows.append(row)
        for number, row in enumerate(rows):
            csv_info.append([number] + row)
        return csv_info

    def make_csv(self):
        with open(self._outfile, "wb") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            for row in self.run():
                writer.writerow(row)

    def _get_department(self, dataset):
        try:
            dpt = dataset['metadata']['custom_fields']['Additional Information']['Department']
        except:
            dpt = "No Department Information"
        return dpt.encode('utf-8')

    def _get_null_count(self, col):
        try:
            total = col['cachedContents']['null']
        except:
            total = "None"
        return total

    def _get_non_null_count(self, col):
        try:
            total = col['cachedContents']['non_null']
        except:
            total = "None"
        return total

    def _get_top(self, col):
        """This gets the top item from cachedContents.  
        Currently the item is returned as a string representation,
        which is less than ideal, but it works.

        """
        try:
            top = col['cachedContents']['top'][0]['item']
        except:
            top = "None"
        return repr(top)
    
    def _analyze_dataset(self, dataset):
        """Analyze a dataset (dict) and return a list of rows.
        """
        # TODO find a cleaner way to deal with encoding issues
        rows = []
        dataset_id = dataset['id']
        dataset_name = dataset['name'].encode('utf-8')
        dataset_dpt = self._get_department(dataset)

        for col_num, col in enumerate(dataset['columns']):
            rows.append([dataset_id, dataset_dpt, dataset_name])
            rows[col_num].append(col['position'])
            rows[col_num].append(col['name'].encode('utf-8'))
            rows[col_num].append(col['fieldName'].encode('utf-8'))
            rows[col_num].append(col['id'])
            rows[col_num].append(col['tableColumnId'])
            rows[col_num].append(col['dataTypeName'].encode('utf-8'))
            rows[col_num].append(col['renderTypeName'].encode('utf-8'))
            rows[col_num].append(self._get_null_count(col))
            rows[col_num].append(self._get_non_null_count(col))
            rows[col_num].append(self._get_top(col))
            rows[col_num].append("SNAPSHOT_DATE_TIME") # placeholder
            rows[col_num].append("IS_CURRENT")         # placeholder
        return rows

if __name__ == "__main__":
    filename = "datasets.json"
    outfile = "out.csv"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]

    Analyzer = DatasetAnalyzer(filename, outfile)
    Analyzer.make_csv()
