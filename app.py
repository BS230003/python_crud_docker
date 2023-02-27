
import base64
import sqlite3, os
from flask import Flask , render_template, request, redirect, session
from werkzeug.utils import secure_filename

# call from different file function
from mongo_db_init import readMongoDBRecord, addMongoDBRecord, deleteMongoDBRecord, updateMongoDBRecord


app = Flask(__name__)
print ("app created with Flask. ", __name__)


# File upload code from the browser
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def readMyName():
    print ('getMyName called')
    return

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    print ("db_connection opened now ")
    return conn

def readDatabase():
    #print ('called readDatabase ??? ')
    conn = get_db_connection()
    global posts
    posts = conn.execute('SELECT * FROM posts').fetchall() 
    #print ("app.py 2 db conn closed")
    #conn.close()
     
    print ("app.py readDatabase() def index SQL query done, Launch now index.xml >>>>> " , len (posts))
    return render_template('index.html', posts=posts)
    #return posts

def readDatabase1():
    conn = get_db_connection()
    global posts
    posts = conn.execute('SELECT * FROM posts').fetchall() 
    #conn.close()
     
    print ("app.py readDatabase1() def index SQL query done, posts returned >>>>> ", len (posts) )
    return posts

def addRecordDatabase(tl, ct):
    conn = get_db_connection()
    conn.execute("INSERT INTO posts (title, content) VALUES ('" + tl + "', '" + ct +"')") 
    print ("app.py db conn commit closed after INSERT ")
    conn.commit()
    conn.close()
    
    print ("app.py: INSERT DONE ==> Launch now index.xml >>>>> " )
    
def deleteRecordDatabase(inp):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE TITLE ='" + inp + "'") 
    print ("app.py db conn commit closed after delete ")
    conn.commit()
    conn.close()
    
    print ("app.py: DELETE DONE ==> Launch now index.xml >>>>> " )

# Set a secret key for encrypting session data
app.secret_key = 'my_secret_key'
 
# dictionary to store user and password
users = {
    'user1': '1',
    'user2': 'password2'
}


# The router is defined here 
@app.route('/')
def gotoIndex ():
    return render_template('index.html')

# calling read page using render_template
@app.route('/read')
def view_form():
    print ('view form called read MongoDB..')
    all_s = readMongoDBRecord ('Bahadur') 
    print ('view form called SQLiteDB..')
    all_p = readDatabase1 ()
    return render_template('read.html', all_students=all_s, posts=all_p) 
 
#calling add.hml page 
@app.route('/add')
def view_form1():
    
    all_p = readDatabase1 ()
    return render_template('add.html', posts=all_p)
 

# For handling get request form we can get
# the form inputs value by using args attribute.
# this values after submitting you will see in the urls.
# e.g http://127.0.0.1:5000/handle_get?username=xxx&password=yyyy223344
# this exploits our credentials so that's
# why developers prefer POST request.
@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        #print ('got to GET')
        #username = request.args['username']
        actionType = request.args['actionType']
        print(" in GET " ,  actionType)
        return readDatabase ()
    else:
        return render_template('index.html')

# Data sent from the client is not exposed into the URL of POST request 
@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        actionType = request.form['actionType']
        
        print(' ==> actionType ' + actionType)
        if (actionType == 'addRecordSQL') : addRecordDatabase (title, content)
        if (actionType == 'deleteRecordSQL') : deleteRecordDatabase (title)
        # MongoDB functions
        if (actionType == 'deleteRecordMongoDB') : deleteMongoDBRecord (title)
        if (actionType == 'addRecordMongoDB') : addMongoDBRecord (title, content)
        
        return readDatabase()
    else:
        return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Router upload for posting a file from browser. File saved local on server and can
# be uploaded to Mongo DB using pymongo library. 

@app.route ('/upload', methods=['POST'])
def uploadFile ():
    #print ('>>> upload file started')
    name = request.form ['title']
    file = request.files['file']
    print ('>>> upload file started', file, name)
    #and allowed_file(file.name)
    if (file ):
        #print ('inside if')
        filename = secure_filename (file.filename)
        #print ('>>>>filename ' + file.filename)
        file.save (os.path.join (app.config['UPLOAD_FOLDER'], filename))
        print ('>>> file saved.', filename)

        img_file = open('./uploads/' + filename, "rb")
        my_string = base64.b64encode(img_file.read()).decode ('utf-8')
        #print(my_string)

        # my string is base64 data
        updateMongoDBRecord (name, my_string)    
        return render_template('index.html',filename=filename)
    else:
        return gotoIndex

if __name__ == '__main__':
    app.run()

# Created by Bahadur Singh singh.bahadur@gmail.com
 
