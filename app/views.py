from app import app
import os
import socket
import json
import urllib2
from flask import render_template, flash, redirect, url_for, abort, send_file, request
from werkzeug import secure_filename
from .forms import PageForm
from flask.ext.autoindex import AutoIndex

# Return a generic static HTML page as base page
@app.route("/")
def index():
	return render_template('index.html', title='Home', links=site_map_links())

# Show directory of files for download
@app.route('/files/', defaults={'req_path': ''})
@app.route('/files/<path:req_path>')
@app.route('/files')
def files(req_path):
    BASE_DIR = 'app/files'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
		# return "req_path: " + req_path + "<br><br>abs_path: " + abs_path
		return send_file('files/' + req_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files, links=site_map_links())

# Example form
@app.route("/form", methods = ['GET', 'POST'])
def form():
	form = PageForm()
	if form.validate_on_submit():
		FormTextField = form.FormTextField.data
		return render_template('formreturn.html', title='Form Return', textfield=FormTextField, links=site_map_links())
	return render_template('formentry.html', title='Form Entry', form=form, links=site_map_links())

# Generates page with a list of all @app.route's
@app.route("/site-map")
def site_map():
    return render_template("site_map.html", links=site_map_links())

def site_map_links():
	links = []
	for rule in app.url_map.iter_rules():
		# Filter out rules we can't navigate to in a browser
		# and rules that require parameters
		if "GET" in rule.methods and len(rule.arguments)==0:
			url = url_for(rule.endpoint, **(rule.defaults or {}))
			links.append((url, rule.endpoint))
	return links

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']