# Simple list of reading items, here as URIs
# Shows how to build a web framework with database connectivity and templates
import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template
from flask_sqlalchemy import SQLAlchemy
import json

 
app = Flask(__name__)

# Check if we are on Bluemix, then get service information from VCAP environment
if 'VCAP_SERVICES' in os.environ:
   dbInfo = json.loads(os.environ['VCAP_SERVICES'])['user-provided'][0]
   dbURI = dbInfo["credentials"]["url"]
   app.config['SQLALCHEMY_DATABASE_URI']=dbURI
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# we are local, so load info from a file
else:
   app.config.from_pyfile('readapp.cfg')


db = SQLAlchemy(app)
 
# Simple data model (object type) resembling an entry on a reading list
# ID, short name or description, an URI and date it was added to the list
# * This could be extended by an attribute whether it has been read
# * Could add categories to it or topics
class Readlist (db.Model):
    __tablename__ = 'readlist'
    id = db.Column('rid', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    uri = db.Column(db.String(200))
    add_date = db.Column(db.DateTime)
 
    def __init__(self, title, text):
        self.name = title
        self.uri = text
        self.add_date = datetime.utcnow()
 
# Our title/index page shows the items on the reading list, so
# we have to grab them sorted by the date they were added.
@app.route('/')
def index():
	return render_template('index.html',
	   items=Readlist.query.order_by(Readlist.add_date.desc()).all()
	)

# Add a new item by rendering a form, obtaining the input values and persisting
# a new object (add and commit the new item).
# Once done we are moving back to the index page that shows all items. 
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Short title is required', 'error')
        elif not request.form['text']:
            flash('URI is required', 'error')
        else:
            item = Readlist(request.form['title'], request.form['text'])
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('new.html')

# This is a "secret" init page that can be called to initialize an empty database
# with our "readlist" table. The table structure is defined above through the model.
@app.route('/init')
def init():
	db.drop_all()
	db.create_all()
	return 'ok, go to <a href="/">home</a>'


# Simple route to test the app. It does not use a template, just returns a string.
@app.route('/hello')
def hello():
    return "Hello folks, this is Python with Flask on Bluemix!"

# Start the app, port is 5000 for local or what Bluemix tells us
# Use the following line instead of the last line if you need to debug
#       app.run(host='0.0.0.0', port=int(port), debug=True)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=int(port))
