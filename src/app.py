from flask import Flask, render_template, send_from_directory, request, redirect
from pymongo import MongoClient
import os


app = Flask(__name__)

app.secret_key = 'key'

logged = True

client = MongoClient('mongodb://localhost:27017')
db = client.wadDB
app.config['UPLOAD_FOLDER'] = 'upload'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form['user']
        password = request.form['pwd']
        result = db.info.find_one({"user": user})
        try:
            if password == result["password"]:
                logged = True
                return redirect('cabinet')
        except:
            e = "login or password wrong"
    else:
        return render_template('login.html')
    return render_template('login.html')

@app.route('/cabinet')
def cabinet():
    if logged == True:
        return render_template('cabinet.html')
    else:
        return render_template('login.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/img/<path:path>')
def index2(path):
    return send_from_directory('static/images', path)


@app.route('/static/<path:path>')
def index3(path):
    return app.send_static_file(path)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/createUser', methods=['POST'])
def createUser():
    email = request.form['email']
    pwd = request.form['pwd']
    user = request.form['user']
    db.info.insert({"user": user, "password": pwd, "email": email})
    return render_template('login.html',user = user)


if __name__ == '__main__':
    app.run(threaded=True, port='5000')
