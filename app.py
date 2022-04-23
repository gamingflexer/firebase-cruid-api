from crypt import methods
from distutils.log import debug
from logging import exception
import os
from os.path import join
import time
import pyrebase
from pexpect import ExceptionPexpect
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app, storage
from flask_cors import CORS, cross_origin
from model import ocr,spacy_700
#from config import config_firebase
import random as ran

# Initialize Flask App
app = Flask(__name__)
CORS(app, support_credentials=True)

# Initialize Firestore DB
try:
    cred = credentials.Certificate("path of json file")
    #default_app = initialize_app(cred, {'storageBucket': 'dp-demo-ca57a.appspot.com'})
    default_app = initialize_app(cred)
    db = firestore.client()
    todo_ref = db.collection('files')
    firebase_storage = pyrebase.initialize_app(config_firebase)
    storage = firebase_storage.storage()
except:
    print("Not Logged in !")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)

def getFileContent(path_dir):
    return_Dict = []
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if root in path_dir:
                f=open(os.path.join(root, file),'rb')
                f.close()
                return_Dict.append(f.name)
    return return_Dict


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# #Upload API
# @app.route('/upload=<string:fileName>', methods=["POST", "GET"])
# def upload(fileName):
#     try:
#         bucket = storage.bucket()
#         blob = bucket.blob(fileName)
#         blob.upload_from_filename(fileName)
#         blob.make_public()
#         return f"PUBLIC - file url, {blob.public_url}"
#     except exception as e:
#         return f"expection occured - {e}"
    
#Index
@app.route('/index')
def index():
    context = { 'server_time': format_server_time() }
    return render_template('index.html', context=context)

#List of Files
@app.route('/list',methods=["POST", "GET"])
def filename(): #get file name
    try:
        all_files = storage.list_files()
        for i in all_files:
            i.download_to_filename(f'download file path{i.name}')
        
        path_list = getFileContent(path_dir = r"to save file path")
        for i in path_list:
            data = ocr(i)
            json = spacy_700(data)
            print(json)
            id = str(ran.randint(0,99999999))
            todo_ref.document(id).set(json)
        return jsonify({"success": True}), 200
    except:
        return jsonify({"Failed": False}), 200  
    


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True,port=port,debug=True)