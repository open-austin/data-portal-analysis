import json
import csv
import dataset
import datetime
import logging

logging.getLogger()


class ViewAnalyzer(object):
    """class ViewAnalyzer()
    Analyzes a list of views and creates a CSV file with the results.
    """
    def __init__(self, db_url = "sqlite://"):
        """Initializes a view analyzer.
        The _generated_headers list contains headers for columns that contain
        data created by the analyzer. There must be an ordered one-to-one
        correspondence between this list and the append operations in
        ViewAnalyzer._analyze_view - see the comments in that function
        for details.
        """
        self._db_url = db_url
        # TODO: Find a better way to deal with generated headers
        self._views = []
        self._generated_headers = ["is_current", "report_creation_time"]
        cur_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        self._creation_time = cur_time
        self._rows = []

    @property
    def creation_time(self):
        """Getter for _creation_time"""
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value):
        """Setter for _creation_time"""
        self._creation_time = value

    def add_view(self, view):
        """Add a view to the analyzer unless it is a duplicate, in which
        case the event is logged and the view is not added.
        """
        if view['id'] in self._views:
            logging.warn("View already analyzed: {0}".format(view['id'].encode('utf8')))
        self._rows.extend(self._analyze_view(view))
        self._views.append(view['id'])

    def _analyze_view(self, view):
        """Analyze a view (dict) and return a list of rows.
        """
        logging.debug("Analyzing {0}: {1}".format(view['id'].encode('utf8'), view['name'].encode('utf8')))

        rows = []
        view_info = self._get_view_info(view)
        if 'columns' not in view.keys():
            logging.warn("No columns in {0}".format(view['id'].encode('utf8')))
            raise KeyError("No Columns")
        for col in view['columns']:
            current_row = []
            current_row.extend(view_info)
            current_row.extend(self._get_column_info(col, view_info[0]))
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
        view_time = self._get_date_time(view)
        view_name = view['name']
        view_id  = view['id']
        try:
            custom = view['metadata']['custom_fields']
            department = custom['Additional Information']['Department']
        except(KeyError):
            department = "null"
            logging.debug("No department information for view {0}".format(view_id.encode('utf8')))

        view_list = [view_id, view_name, department, view_time]
        view_record = dict(view_id = view['id'],
                           view_name = view['name'],
                           view_dpt = department,
                           view_time = view['createdAt'],
                           last_modified = view['viewLastModified'])

        self._store_view_to_db(view_record)        
        return view_list

    def _store_view_to_db(self, record):
        with dataset.connect(self._db_url) as db:
            table = db.get_table('views', primary_id = 'view_id', primary_type = 'String')
            try:
                table.insert(record)
            except:
                current_record = table.find_one(view_id = record['view_id'])
                if int(current_record['last_modified']) < int(record['last_modified']):
                    table.update(record, ['view_id'])
                else:
                    return
    
    def _get_column_info(self, col, view_id):
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
        self._store_col_to_db(col, view_id)
        return current_row
    
    def _store_col_to_db(self, col, view_id):
        record = dict(parent_view_id = view_id,
                      tableColumnId = col['tableColumnId'],
                      position = col['position'],
                      name = col['name'],
                      fieldName = col['fieldName'],
                      col_id = col['id'],
                      dataTypeName = col['dataTypeName'],
                      renderTypeName = col['renderTypeName'])
        
        with dataset.connect(self._db_url) as db:
            table = db.get_table('columns', primary_id = 'tableColumnId', primary_type = 'String')
            try:
                table.insert(record)
            except:
                table.update(record, ['tableColumnId'])

        
    @staticmethod
    def _get_date_time(view):
        """This function fills the snapshot_date_time column.
        """
        if view['createdAt'] == "created_at":
            return "created_at"
        try:
            epoch_time = float(view['createdAt'])
            date_time = datetime.datetime.utcfromtimestamp(
                epoch_time).replace(microsecond=0).isoformat()
        except(KeyError):
            logging.warn("snapshot_time not found for view {0}".format(view['id'].encode('utf8')))
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
