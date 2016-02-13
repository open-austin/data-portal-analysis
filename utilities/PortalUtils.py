import json
import csv
import datetime
import logging

logging.getLogger()


class ViewAnalyzer(object):
    """class ViewAnalyzer()
    Analyzes a list of views and creates a CSV file with the results.
    """
    def __init__(self):
        """Initializes a view analyzer.
        The _generated_headers list contains headers for columns that contain
        data created by the analyzer. There must be an ordered one-to-one
        correspondence between this list and the append operations in
        ViewAnalyzer._analyze_view - see the comments in that function
        for details.
        """
        # TODO: Find a better way to deal with generated headers
        self._views = []
        self._generated_headers = ["is_current", "report_creation_time"]
        cur_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        self._creation_time = cur_time
        self._rows = []

    @property
    def creation_time(self):
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value):
        self._creation_time = value

    def add_view(self, view):
        """Add a view to the analyzer unless it is a duplicate, in which
        case the event is logged and the view is not added.
        """
        if view['id'] in self._views:
            logging.warn("View already analyzed: %s" % view['id'])
            return
        else:
            self._rows.extend(self._analyze_view(view))
            self._views.append(view['id'])

    def _analyze_view(self, view):
        """Analyze a view (dict) and return a list of rows.
        """
        logging.debug("Analyzing %s: %s"
                      % (view['id'], view['name']))

        rows = []
        view_info = self._get_view_info(view)
        if 'columns' not in view.keys():
            logging.warn("No columns in %s" % view['id'])
            raise KeyError("No Columns")
        for col in view['columns']:
            current_row = []
            current_row.extend(view_info)
            current_row.extend(self._get_column_info(col))
            # Generated headers must correspond to the following append calls
            current_row.append(u"IS_CURRENT")
            current_row.append(self._creation_time)

            encoded_row = []  # CSV writer requires unicode
            for item in current_row:
                if isinstance(item, unicode):
                    item = item.encode('utf-8')
                encoded_row.append(item)

            rows.append(encoded_row)
        return rows

    def _analyze_all(self):
        """Run the analyzer on all views and return the results.
        """
        results = []
        for item in self._views:
            try:
                analyzed_content = self._analyze_view(item)
            except(KeyError):
                continue
            for row in analyzed_content:
                results.append(row)
        return results

    def _get_view_info(self, view):
        """Returns view info (common to all columns) as a list.
        """
        view_id = view['id']
        view_name = view['name']
        view_time = self._get_date_time(view)
        try:
            custom = view['metadata']['custom_fields']
            view_dpt = custom['Additional Information']['Department']
        except:
            view_dpt = "null"
            logging.debug("No department information for view %s"
                          % view_id)

        return [view_id, view_name, view_dpt, view_time]

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

    def _get_date_time(self, view):
        """This function fills the snapshot_date_time column.
        """
        if view['createdAt'] == "created_at":
            return "created_at"
        try:
            epoch_time = float(view['createdAt'])
            date_time = datetime.datetime.utcfromtimestamp(
                epoch_time).replace(microsecond=0).isoformat()
        except(KeyError):
            logging.warn("snapshot_time not found for view %s"
                         % view['id'])
            date_time = "null"
        return date_time

    def get_headers(self):
        """Generate column headers by analyzing a custom view.
        """
        with open("utilities/headers.json") as headerfile:
            headerset = json.loads(headerfile.read())
            headers = ['id']
            headers.extend(self._analyze_view(headerset)[0][:-2])
            headers.extend(self._generated_headers)
            return headers

    def make_csv(self, filename=None):
        """Utility function for writing the report to a CSV file.
        """
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
