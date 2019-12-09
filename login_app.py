# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:18:19 2019

@author: naveenn
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import time

app = Flask(__name__)
os.chdir(r'C:\Users\Public\Documents\Python Scripts\Attendence_system')

UPLOAD_FOLDER = 'C:/Users/Public/Documents/Python Scripts/Attendence_system/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        user_id = request.form['login']
        password = request.form['password']
#        person = request.form['person']
        
        if(user_id != 'admin' or password != 'admin'):
            error = 'Invalid Credential'
        else:
            return redirect(url_for('second_page'))
        
        return render_template('login.html', error = error)
     
@app.route('/second_page')
def second_page():
    return render_template('second_page.html')

@app.route('/webcam', methods=['GET', 'POST'])
def webcam_img():
    return render_template('webcam.html')

@app.route('/image', methods=['GET', 'POST'])
def imageForm():
    if request.method == 'POST':
        file = request.files['image']
        global visitor_ID
        tempname = ('%s.jpeg' % time.strftime("%Y_%m_%d_%H_%M_%S"))
        visitor_ID = tempname
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], tempname))
        return render_template('webcam.html')

@app.route('/upload', methods=['GET', 'POST'])
def img_upload():
    file = request.files['image_uploads']
    global visitor_ID
    tempname = ('%s.jpeg' % time.strftime("%Y_%m_%d_%H_%M_%S"))
    visitor_ID = tempname
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], tempname))
    
    return ""
    

if __name__ == '__main__':
    app.run(debug = True)


