# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:51:32 2019

@author: naveenn
"""

from flask import Flask, request, render_template
import time
import os
#import pandas as pd
#from datetime import datetime

UPLOAD_FOLDER = 'C:/Users/Public/Documents/Python Scripts/Attendence_system/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def user():
    return render_template('webcam.html')

@app.route('/image', methods=['GET', 'POST'])
def imageForm():
    if request.method == 'POST':
        file = request.files['image']
        global visitor_ID
        tempname = ('%s.jpeg' % time.strftime("%Y_%m_%d_%H_%M_%S"))
        visitor_ID = tempname
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], tempname))
        return ''

if __name__ == '__main__':
    app.run(debug = True, port = 5000)
    
    
    