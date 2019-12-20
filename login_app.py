# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:18:19 2019

@author: naveenn
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import pandas as pd
import numpy as np
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
        # Storing as an excel file
        df_excel = df.copy()
        def color_negative_red(val):
            color = 'red' if val == 'Absent' else 'black'
            return 'color: %s' % color
         
        df_excel.style.applymap(color_negative_red).to_excel(os.path.join('Attendance_sheet', class_name, (batch+'.xlsx')), index = False, engine = 'openpyxl', header = True)
        # Storing as CSV file
        df.to_csv(os.path.join('Attendance_sheet', class_name, (batch+'.csv')), index = False)

        # Leave count
        # Today absenties
        today_abs = list(df.loc[df[df.columns[-1]] == 'Absent','Name'])
        leave_numbers = []
        for name in today_abs:
            i = -1
            cnt = 0
            while(i > -9):
                if(list(df.loc[df['Name'] == name, df.columns[i]])[0] == 'Absent'):
                    cnt = cnt+1
                    i = i-1
                else:
                    break
            leave_numbers.append(cnt)    
        leave_numbers = [str(7)+'+ Days' if leave_num >= 8 else leave_num for leave_num in leave_numbers]
        abs_cnt_df = pd.DataFrame(list(zip(today_abs,leave_numbers)), columns = ['Name', 'Number of Days'], index = range(1, len(leave_numbers)+1))
        
        # Last day absenties
        lst_day_abs = list(df.loc[df[df.columns[-2]] == 'Absent','Name'])
        leave_numbers = []
        for name in lst_day_abs:
            i = -2
            cnt = 0
            while(i > -9):
                if(list(df.loc[df['Name'] == name, df.columns[i]])[0] == 'Absent'):
                    cnt = cnt+1
                    i = i-1
                else:
                    break
            leave_numbers.append(cnt)    
        leave_numbers = [str(7)+'+ Days' if leave_num >= 8 else leave_num for leave_num in leave_numbers]
        lstday_abs = pd.DataFrame(list(zip(lst_day_abs,leave_numbers)), columns = ['Name', 'Number of Days'], index = range(1, len(leave_numbers)+1))
          
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
        cnt_abs = []
        cnt_pre = []
        for col in df.iloc[:,1:]:
            if(df[col].value_counts()[0] != len(df)):
                cnt_abs.append(df[col].value_counts()['Absent'])
                cnt_pre.append(df[col].value_counts()['Present'])
            else:
                if(df[col].value_counts().index[0] == 'Absent'):
                    cnt_abs.append(df[col].value_counts()[0])
                    cnt_pre.append(0)
                else:
                    cnt_pre.append(df[col].value_counts()[0])
                    cnt_abs.append(0)    
        
        width = 0.25
        fig = plt.figure(figsize=(10,7))
        ax = fig.subplots(1,1)
        
        # Set position of bar on X axis
        r1 = np.arange(len(cnt_abs[-7:]))
        r2 = [x + width for x in r1]
        #        r3 = [x + barWidth for x in r2]

        ax.bar(r1, cnt_pre[-7:], color='#557f2d', width=width, edgecolor='white', label='Present')
        ax.bar(r2, cnt_abs[-7:], color='#F94242', width=width, edgecolor='white', label='Absent')
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        plt.xticks([r + width for r in range(len(cnt_abs))], list(df.columns[1:])[-7:])
        ax.tick_params(axis ='x', rotation = 45)
 
        # Create legend & Show graphic
        ax.legend()
#        ax.bar(df.columns[1:][-7:], cnt[-7:], width, color = 'b')

        ax.set_title('Past 7 days data', bbox={'facecolor':'0.8', 'pad':5})
        
        fg = ax.get_figure()
        plt.savefig(graph_path+'bar_chart'+d)
        plt.close(fg)
        plt.close(fig)
        
        print("Image saved")
        return render_template('preview.html',  tables=[df.iloc[:,-7:].to_html(columns = df.iloc[:,-7:].columns,
                                                            header = "true", border = 10), 
                                                        abs_cnt_df.to_html(columns = abs_cnt_df.columns,
                                                            header = "true", border = 10),
                                                        lstday_abs.to_html(columns = lstday_abs.columns,
                                                            header = "true", border = 10)],
                                                titles = ['na', 'Attendance Sheet', 'Absenties Today', 'Absenties Last_day'],                       
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
        df_excel = df.copy()

        def color_negative_red(val):
            color = 'red' if val == 'Absent' else 'black'
            return 'color: %s' % color
         
        df_excel.style.applymap(color_negative_red).to_excel(os.path.join('Attendance_sheet', class_name, (batch+'.xlsx')), index = False, engine = 'openpyxl', header = True)

        df.to_csv(os.path.join('Attendance_sheet', class_name, (batch+'.csv')), index = False)
        
        # Leave count
        # Today absenties
        today_abs = list(df.loc[df[df.columns[-1]] == 'Absent','Name'])
        leave_numbers = []
        for name in today_abs:
            i = -1
            cnt = 0
            while(i > -9):
                if(list(df.loc[df['Name'] == name, df.columns[i]])[0] == 'Absent'):
                    cnt = cnt+1
                    i = i-1
                else:
                    break
            leave_numbers.append(cnt)    
        leave_numbers = [str(7)+'+ Days' if leave_num >= 8 else leave_num for leave_num in leave_numbers]
        abs_cnt_df = pd.DataFrame(list(zip(today_abs,leave_numbers)), columns = ['Name', 'Number of Days'], index = range(1, len(leave_numbers)+1))
        
        # Last day absenties
        lst_day_abs = list(df.loc[df[df.columns[-2]] == 'Absent','Name'])
        leave_numbers = []
        for name in lst_day_abs:
            i = -2
            cnt = 0
            while(i > -9):
                if(list(df.loc[df['Name'] == name, df.columns[i]])[0] == 'Absent'):
                    cnt = cnt+1
                    i = i-1
                else:
                    break
            leave_numbers.append(cnt)    
        leave_numbers = [str(7)+'+ Days' if leave_num >= 8 else leave_num for leave_num in leave_numbers]
        lstday_abs = pd.DataFrame(list(zip(lst_day_abs,leave_numbers)), columns = ['Name', 'Number of Days'], index = range(1, len(leave_numbers)+1))
        
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
        
        fig = plt.figure(figsize=(6,6))
        ax = fig.subplots(1,1)
        # Pie chart
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        ax.set_title("Present Vs Abscenties count\n" + str(date.today()), bbox={'facecolor':'0.8', 'pad':5})
        fg = ax.get_figure()
        plt.savefig(graph_path+'pie_chart'+d)
        plt.close(fg)
        plt.close(fig)        
        
        # Bar chart
        cnt_abs = []
        cnt_pre = []
        for col in df.iloc[:,1:]:
            if(df[col].value_counts()[0] != len(df)):
                cnt_abs.append(df[col].value_counts()['Absent'])
                cnt_pre.append(df[col].value_counts()['Present'])
            else:
                if(df[col].value_counts().index[0] == 'Absent'):
                    cnt_abs.append(df[col].value_counts()[0])
                    cnt_pre.append(0)
                else:
                    cnt_pre.append(df[col].value_counts()[0])
                    cnt_abs.append(0)    
        
        width = 0.25
        fig = plt.figure(figsize=(10,7))
        ax = fig.subplots(1,1)
        
        # Set position of bar on X axis
        r1 = np.arange(len(cnt_abs[-7:]))
        r2 = [x + width for x in r1]
        #        r3 = [x + barWidth for x in r2]

        ax.bar(r1, cnt_pre[-7:], color='#557f2d', width=width, edgecolor='white', label='Present')
        ax.bar(r2, cnt_abs[-7:], color='#F94242', width=width, edgecolor='white', label='Absent')
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        plt.xticks([r + width for r in range(len(cnt_abs))], list(df.columns[1:])[-7:])
        ax.tick_params(axis ='x', rotation = 45)
 
        # Create legend & Show graphic
        ax.legend()
#        ax.bar(df.columns[1:][-7:], cnt[-7:], width, color = 'b')

        ax.set_title('Past 7 days data', bbox={'facecolor':'0.8', 'pad':5})
        
        fg = ax.get_figure()
        plt.savefig(graph_path+'bar_chart'+d)
        plt.close(fg)
        plt.close(fig)
        
        return render_template('preview.html',  tables=[df.iloc[:,-7:].to_html(columns = df.iloc[:,-7:].columns,
                                                            header = "true", border = 10), 
                                                        abs_cnt_df.to_html(columns = abs_cnt_df.columns,
                                                            header = "true", border = 10),
                                                        lstday_abs.to_html(columns = lstday_abs.columns,
                                                            header = "true", border = 10)],
                                                titles = ['na', 'Attendance Sheet', 'Absenties Today', 'Absenties Last_day'],                       
                                                img_pie = graph_path+'pie_chart'+d,
                                                img_bar = graph_path+'bar_chart'+d)


if __name__ == '__main__':
    app.run(debug = True)


#df = pd.read_csv(r'C:\Users\Public\Documents\Python Scripts\Attendence_system\Attendance_sheet\BSc_Computer\2017-20.csv')
####df.iloc[:,-4:]
#df = df.set_index('Name', drop = True)
###del df.index.name
##
