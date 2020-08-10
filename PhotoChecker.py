# project-2 Stocker Picker App
# Tanvir Khan, Nicky Pant, Paul Pineda, James Ye, Fabienne Zumbuehl

import os
from flask import Flask, jsonify
import datetime as dt
from flask import Flask, render_template, redirect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return render_template('landing.html')

@app.route("/photochecker")
def photochecker():
    imagefile = "testing"
    data = get_beauty_score(imagefile)
    return render_template('photochecker.html', data=data)

@app.route("/about")
def about():
    return render_template("about.html")


def get_beauty_score(imageFile):
    data = {"beautyscore", 4}
    return data


# this part must be placed at the end of the file!!	
if __name__ == '__main__':
    app.run(debug=True)
