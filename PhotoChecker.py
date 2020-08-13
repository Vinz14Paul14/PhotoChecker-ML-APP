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
from config import s3_bucket
from config import SECRET_KEY
import BeautyScore
import S3handler
import RekognitionHandler


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

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

@app.route('/photoreport/<filename>')
def check_photo(filename):
    if not S3handler.check_file(filename):
        return render_template('filenotfound.html', data=filename)
    imageS3url = f"https://{s3_bucket}.s3.amazonaws.com/{filename}"
    data = BeautyScore.get_beauty_score(imageS3url)
    data["filename"] = filename
    data["imageS3url"] = imageS3url
    data['celebrityData'] = RekognitionHandler.recognize_celebrities(filename)
    data['labelsData'] = RekognitionHandler.detect_labels(filename)
    data['unsafeData'] = RekognitionHandler.detect_unsafeContent(filename)
    
    # put detect_faces last because we will edit the photo on this call
    data['faceData'] = RekognitionHandler.detect_faces(filename)
    
    return render_template('photoreport.html', data=data)
    
@app.route("/photochecker", methods=['POST'])
def upload_file():
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
        #print(filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        S3handler.upload_file_to_s3(file, filename=filename, content_type=file.content_type)
        redirect_url = url_for('check_photo', filename=filename)
        #print(f"redirect_url={redirect_url}")
        return redirect(redirect_url)
    else:
        flash('File type not allowed')
        return redirect(request.url)
    

@app.route("/photochecker", methods=['GET'])
def photochecker():
    return render_template('photochecker.html')

@app.route("/about")
def about():
    return render_template("about.html")

# this part must be placed at the end of the file!!	
if __name__ == '__main__':
    app.run(debug=True)
