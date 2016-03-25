import dataset
import datetime
import logging
from flask import Flask
from flask import render_template
import os
working_dir = os.path.dirname(os.path.realpath(__file__))
database_location = os.path.join(working_dir, "portal.db")
database_url = "sqlite:///" + database_location

app = Flask(__name__, template_folder=working_dir)

def convert_time(timestamp):
    return datetime.datetime.utcfromtimestamp(float(timestamp)).isoformat()

@app.route('/')
@app.route('/<offset>')
def offset_index(offset = 0):
    with dataset.connect(database_url, row_type=dict) as db:
        table = db.get_table('views')
    view_list = table.find(_limit=10, _offset = offset, order_by='-last_modified')
    modified_view_list = []
    for view in view_list:
        modified_view = view
        modified_view['last_modified'] = convert_time(view['last_modified'])
        modified_view['view_time'] = convert_time(view['view_time'])
        modified_view_list.append(modified_view)
    next_offset = str(int(offset)+10)
    previous_offset = str(int(offset)-10)
    if int(offset) <= 10:
        previous_offset = '0'
    if int(offset) == 0:
        previous_offset = None
    return render_template('static/index.html', previous_offset = previous_offset, next_offset=next_offset,view_list=modified_view_list)

# def index():
#     with dataset.connect(database_url, row_type=dict) as db:
#         table = db.get_table('views')
#     view_list = table.find(_limit=10, order_by='-last_modified')
#     return render_template('static/index.html', view_list=view_list)


if __name__ == '__main__':
    app.run(debug=True)
