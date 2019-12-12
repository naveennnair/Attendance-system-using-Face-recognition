# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:18:19 2019

@author: naveenn
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import pandas as pd
import time
from datetime import date
from face_detection import student_face_identifier as sfi

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

@app.route('/Class_selection', methods = ['POST','GET'])
def select_class():
    if request.method == 'POST':
        global class_name, batch
        class_name = request.form['class_name']
        batch = request.form['batch_name']
        return render_template('second_page.html')
     
@app.route('/index')
def second_page():
    return render_template('index.html')

@app.route('/webcam', methods=['GET', 'POST'])
def webcam_img():
    return render_template('webcam.html')

@app.route('/image', methods=['GET', 'POST'])
def imageForm():
    if request.method == 'POST':
        file = request.files['image']
        global visitor_ID
        global names
        tempname = ('%s.jpeg' % time.strftime("%Y_%m_%d_%H_%M_%S"))
        visitor_ID = tempname
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], class_name, tempname))
        # Getting latest file
        list_of_files = glob.glob(os.path.join('C:/Users/Public/Documents/Python Scripts/Attendence_system/uploads/',class_name,'*.jpeg'))
        latest_img = max(list_of_files, key=os.path.getctime)
        names = sfi.getting_names(class_name,latest_img)
        # Storing as a DataFrame
        df = pd.read_csv(os.path.join('Student_names', class_name, (batch+'.csv')))
        df[str(date.today())] = 'Absent'
        df[str(date.today())].loc[df['Name'].isin(names),] = 'Present'
        df.to_csv(os.path.join('Student_names', class_name, (batch+'.csv')), index = False)        
        
        return render_template('preview.html',  tables=[df.to_html(classes ='df', header = "true")])

@app.route('/upload', methods=['GET', 'POST'])
def img_upload():
    if request.method == 'POST':        
        file = request.files['image_uploads']
        global visitor_ID
        global names
        tempname = ('%s.jpeg' % time.strftime("%Y_%m_%d_%H_%M_%S"))
        visitor_ID = tempname
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], class_name, tempname))
        # Getting latest file
        list_of_files = glob.glob(os.path.join('C:/Users/Public/Documents/Python Scripts/Attendence_system/uploads/',class_name,'*.jpeg'))
        latest_img = max(list_of_files, key=os.path.getctime)
        names = sfi.getting_names(class_name,latest_img)
        # Storing as a DataFrame
        df = pd.read_csv(os.path.join('Student_names', class_name, (batch+'.csv')))
        df[str(date.today())] = 'Absent'
        df[str(date.today())].loc[df['Name'].isin(names),] = 'Present'
        df.to_csv(os.path.join('Student_names', class_name, (batch+'.csv')), index = False)
        
        return render_template('preview.html',  tables=[df.to_html(classes ='df', header = "true")])



if __name__ == '__main__':
    app.run(debug = True)


