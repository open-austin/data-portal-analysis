import sys
import json

class DatasetAnalyzer():
    def __init__(self, filename):
        data_json = open(filename)
        data_str = data_json.read()
        data_dict = json.loads(data_str)
        self._data_dict = data_dict

    def print_columns(self):
        for item in self._data_dict['datasets']:
            print item['id'], ':', item['name'], '\n'
            for col in item['columns']:
                print col['name']


if __name__ == "__main__":
    filename = "datasets.json"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    Analyzer = DatasetAnalyzer(filename)
    Analyzer.print_columns()



