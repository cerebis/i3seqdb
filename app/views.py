from flask import render_template

from app.myapp import app
from app.myapp import db
from app.objects import *

@app.route('/')
def index():
    session = db.create_scoped_session()
    samples = session.query(Sample).all()
    return render_template('samples.html', samples=samples)
