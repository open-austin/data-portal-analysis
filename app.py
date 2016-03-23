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

@app.route('/')
def index():
    with dataset.connect(database_url, row_type=dict) as db:
        table = db.get_table('views')
    view_list = table.find(_limit=10, order_by='-created_at')
    return render_template('static/index.html', view_list=view_list)

@app.route('/<offset>')
def offset_index(offset = 0):
    with dataset.connect(database_url, row_type=dict) as db:
        table = db.get_table('views')
    view_list = table.find(_limit=10, _offset = offset, order_by='-created_at')
    return render_template('static/index.html', view_list=view_list)


if __name__ == '__main__':
    app.run(debug=True)
