# project-2 Stocker Picker App
# Tanvir Khan, Nicky Pant, Paul Pineda, James Ye, Fabienne Zumbuehl

import os
from flask import Flask, jsonify
import datetime as dt
from flask import Flask, render_template, redirect, flash, request, url_for
from werkzeug.utils import secure_filename
import time
import requests
from flask import send_from_directory
import BeautyScore

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# max upload file size is 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return render_template('landing.html')

# check if file is allowed to be uploaded
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data = BeautyScore.get_beauty_score(filename)
    data["filename"] = filename
    print(data)
    return render_template('score.html', data=data)
    
@app.route("/photochecker", methods=['GET', 'POST'])
def photochecker():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'fileToUpload' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['fileToUpload']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = timestr + filename
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            redirect_url = url_for('uploaded_file', filename=filename)
            print(f"redirect_url={redirect_url}")
            return redirect(redirect_url) 
    return render_template('photochecker.html')

@app.route("/about")
def about():
    return render_template("about.html")

# this part must be placed at the end of the file!!	
if __name__ == '__main__':
    app.run(debug=True)
