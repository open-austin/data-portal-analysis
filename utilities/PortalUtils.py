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
        db_url is the location of the database, defaults is in-memory (not persistent)
        """
        self._db_url = db_url
        cur_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        self._creation_time = cur_time

    @property
    def creation_time(self):
        """Getter for _creation_time"""
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value):
        """Setter for _creation_time"""
        self._creation_time = value

    def add_view(self, view):
        """Analyze a view (dict) and store results in the database.
        """
        logging.debug("Analyzing {0}: {1}".format(view['id'].encode('utf8'), view['name'].encode('utf8')))

        view_record = self._get_view_record(view)
        self._store_view_to_db(view_record)
        
        if 'columns' not in view.keys():
            logging.warn("No columns in {0}".format(view['id'].encode('utf8')))
            raise KeyError("No Columns")

        for col in view['columns']:
            col_record = self._get_col_record(col)
            self._store_col_to_db(col_record, view['id'])
            self._store_unnormalized(view_record, col_record)

    def _get_view_record(self, view):
        """Returns view info (common to all columns) as a list.
        """
        try:
            description = view['description']
        except(KeyError):
            description = 'No description'
            logging.debug("No description for view {0}".format(view['id'].encode('utf8')))
        try:
            attrib = view['attribution']
        except(KeyError):
            attrib = "No attribution"
            logging.debug("No attribution for view {0}".format(view['id'].encode('utf8')))
        try:
            category = view['category']
        except(KeyError):
            category = "No category"
            logging.debug("No category for view {0}".format(view['id'].encode('utf8')))
        try:
            custom = view['metadata']['custom_fields']
            department = custom['Additional Information']['Department']
        except(KeyError):
            department = "No department"
            logging.debug("No department information for view {0}".format(view['id'].encode('utf8')))
            

        view_record = dict(view_id = view['id'],
                           view_name = view['name'],
                           view_dpt = department,
                           view_time = view['createdAt'],
                           last_modified = view['viewLastModified'],
                           view_attrib = attrib,
                           view_description = description,
                           view_category = category)

        return view_record

    def _get_col_record(self, col):
        record = dict(tableColumnId = col['tableColumnId'],
                      position = col['position'],
                      name = col['name'],
                      fieldName = col['fieldName'],
                      col_id = col['id'],
                      dataTypeName = col['dataTypeName'],
                      renderTypeName = col['renderTypeName'])
        return record

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
    
    def _store_col_to_db(self, col_record, view_id):
        with dataset.connect(self._db_url) as db:
            table = db.get_table('columns', primary_id = 'tableColumnId', primary_type = 'String')
            try:
                table.insert(col_record)
            except:
                table.update(col_record, ['tableColumnId'])

        
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

    def _store_unnormalized(self, *records):
        merged_record = {}
        for record in records:
            merged_record.update(record)
        # merged_record['creation_time'] = self._creation_time
        with dataset.connect(self._db_url) as db:
            table = db.get_table('unnormalized', primary_id = 'col_id', primary_type = 'Integer')
            table.upsert(merged_record, ['col_id'])
            
    def make_csv(self, csv_filename=None):
        """Utility function for writing the report to a CSV file.
        """
        with dataset.connect(self._db_url) as db:
            table = db['unnormalized'].all()
            dataset.freeze(table, format='csv', filename=csv_filename)


