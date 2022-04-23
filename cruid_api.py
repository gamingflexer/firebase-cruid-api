# app.py
# Required Imports
from distutils.log import debug
import os
import time
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS, cross_origin


# Initialize Flask App
app = Flask(__name__)
CORS(app, support_credentials=True)
# Initialize Firestore DB
cred = credentials.Certificate('/Users/cosmos/dp-demo-ca57a-firebase-adminsdk-bh0fq-b5d37d24c6.json')
# cred2 = credentials.Certificate("/Users/cosmos/could-gc.json")

default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('files')

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)




@app.route('/index')
def index():
    context = { 'server_time': format_server_time() }
    return render_template('index.html', context=context)


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port,debug=True)