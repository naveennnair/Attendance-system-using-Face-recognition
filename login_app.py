# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:18:19 2019

@author: naveenn
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import pandas as pd
#import numpy as np
import time
from datetime import date
from face_detection import student_face_identifier as sfi
import matplotlib.pyplot as plt

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
        return ""
    
@app.route('/data_preview', methods=['GET', 'POST']) 
def webcam_imgcapture():   
    if request.method == 'POST':
        # Getting latest file
        list_of_files = glob.glob(os.path.join('C:/Users/Public/Documents/Python Scripts/Attendence_system/uploads/',class_name,'*.jpeg'))
        latest_img = max(list_of_files, key=os.path.getctime)
        names = sfi.getting_names(class_name,latest_img)
        # Storing as a DataFrame
        df = pd.read_csv(os.path.join('Attendance_sheet', class_name, (batch+'.csv')))
        df[str(date.today())] = 'Absent'
        df[str(date.today())].loc[df['Name'].isin(names),] = 'Present'
        df.to_csv(os.path.join('Attendance_sheet', class_name, (batch+'.csv')), index = False)
        df = df.set_index('Name')
        del df.index.name
        
        # Getting the Graphs
        d = ('%s.jpg' % time.strftime("%Y%m%d%H%M%S"))
        graph_path = 'static/diagrams/'
        labels = ['Absent', 'Present']

        if(df[str(date.today())].value_counts()[0] != len(df)):
            sizes = [df[str(date.today())].value_counts()['Absent'], df[str(date.today())].value_counts()['Present']]
        else:
            if(df[str(date.today())].value_counts().index[0] == 'Absent'):
                sizes = [df[str(date.today())].value_counts()[0], 0]
            else:    
                sizes = [0, df[str(date.today())].value_counts()[0]]

        colors = ['red', 'yellowgreen']
        explode = (0.1, 0)  # explode 1st slice
        
        fig = plt.figure(figsize=(8,8))
        ax = fig.subplots(1,1)
        # Pie chart
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        ax.set_title("Present Vs Abscenties count\n" + str(date.today()), bbox={'facecolor':'0.8', 'pad':9})
        fg = ax.get_figure()
        plt.savefig(graph_path+'pie_chart'+d)
        plt.close(fg)
        plt.close(fig)        
        
        # Bar chart
        cnt = []
        for col in df.iloc[:,1:]:
            cnt.append(df[col].value_counts()['Absent'])
        
        width = 0.8
        fig, ax = plt.subplots()
                                
        ax.bar(df.columns[1:][-5:], cnt[-5:], width, color = 'b')
        ax.set_ylabel('Absenties Count')
        ax.set_title('Past 5 days data', bbox={'facecolor':'0.8', 'pad':5})
        
        fg = ax.get_figure()
        plt.savefig(graph_path+'bar_chart'+d)
        plt.close(fg)
        plt.close(fig)
        
        print("Image saved")
        return render_template('preview.html',  tables=[df.iloc[:,-7:].to_html(columns = df.iloc[:,-7:].columns,
                                                        classes ='df', header = "true", border = 10, index_names = False)], 
                                                        img_pie = graph_path+'pie_chart'+d,
                                                        img_bar = graph_path+'bar_chart'+d)


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
        df = pd.read_csv(os.path.join('Attendance_sheet', class_name, (batch+'.csv')))
        df[str(date.today())] = 'Absent'
        df[str(date.today())].loc[df['Name'].isin(names),] = 'Present'
        df.to_csv(os.path.join('Attendance_sheet', class_name, (batch+'.csv')), index = False)
        df = df.set_index('Name')
        del df.index.name
        
        # Getting the Graphs
        d = ('%s.jpg' % time.strftime("%Y%m%d%H%M%S"))
        graph_path = 'static/diagrams/'
        labels = ['Absent', 'Present']
        
        if(df[str(date.today())].value_counts()[0] != len(df)):
            sizes = [df[str(date.today())].value_counts()['Absent'], df[str(date.today())].value_counts()['Present']]
        else:
            if(df[str(date.today())].value_counts().index[0] == 'Absent'):
                sizes = [df[str(date.today())].value_counts()[0], 0]
            else:    
                sizes = [0, df[str(date.today())].value_counts()[0]]

#        sizes = [df[str(date.today())].value_counts()[0], df[str(date.today())].value_counts()[1]]
        colors = ['red', 'yellowgreen']
        explode = (0.1, 0)  # explode 1st slice
        
        fig = plt.figure(figsize=(8,8))
        ax = fig.subplots(1,1)
        # Pie chart
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        ax.set_title("Present Vs Abscenties count\n" + str(date.today()), bbox={'facecolor':'0.8', 'pad':9})
        fg = ax.get_figure()
        plt.savefig(graph_path+'pie_chart'+d)
        plt.close(fg)
        plt.close(fig)        
        
        # Bar chart
        cnt = []
        for col in df.iloc[:,1:]:
            cnt.append(df[col].value_counts()['Absent'])
        
        width = 0.8
        fig, ax = plt.subplots()
                                
        ax.bar(df.columns[1:][-5:], cnt[-5:], width, color = 'b')
        ax.set_ylabel('Absenties Count')
        ax.set_title('Past 5 days data', bbox={'facecolor':'0.8', 'pad':5})
        
        fg = ax.get_figure()
        plt.savefig(graph_path+'bar_chart'+d)
        plt.close(fg)
        plt.close(fig)
        
        return render_template('preview.html',  tables=[df.iloc[:,-7:].to_html(columns = df.iloc[:,-7:].columns,
                                                        classes ='df', header = "true", border = 10, index_names = False)], 
                                                        img_pie = graph_path+'pie_chart'+d,
                                                        img_bar = graph_path+'bar_chart'+d)


if __name__ == '__main__':
    app.run(debug = True)


#df = pd.read_csv(r'C:\Users\Public\Documents\Python Scripts\Attendence_system\Attendance_sheet\BSc_Computer\2017-20.csv')
###df.iloc[:,-4:]
##df = df.set_index('Name', drop = False)
##del df.index.name
#
#df[df.columns[-1]].value_counts()
