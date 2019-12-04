# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:18:19 2019

@author: naveenn
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)
os.chdir(r'C:\Users\Public\Documents\Python Scripts\Attendence_system')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/second_page')
def second_page():
    return render_template('second_page.html')

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
     
if __name__ == '__main__':
    app.run(debug = True)
