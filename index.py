from flask import Flask,render_template,request
import numpy as np
from flask_pymongo import PyMongo
import json 
import time

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://sanjiv:pass123@facebookreactions-iwesq.mongodb.net/reactions"
mongo = PyMongo(app)

@app.route('/')
def home():
    cursor = mongo.db.reactions.find({})
    data = []
    for document in cursor:
        current_data = {}
        for key,val in document.items():
            if key=="_id":
                current_data[key]=val
            else:
                key = key.replace('{{{}}}','.')
                current_data[key] = val
        data.append(current_data)    
    return render_template('index.html',data = data)

@app.route('/upload',methods=['GET','POST'])
def add_item():
    if request.method == 'POST':
        array_of_objects= request.form.getlist('array[]')
        if array_of_objects:
            data = [json.loads(s) for s in array_of_objects]
            changedData = []
            for datum in data:
                newData = {}
                for key,val in datum.items():
                    newKey=key.replace('.','{{{}}}')
                    newData[newKey] = val
                changedData.append(newData) 
            mongo.db.reactions.insert_many(changedData)
        return "success"

if __name__=='__main__':
    app.run(debug=True)