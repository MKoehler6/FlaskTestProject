import os

from flask import Flask, url_for, request, render_template, redirect, make_response, escape, session
from werkzeug.utils import secure_filename

app = Flask(__name__)


# einrichten auf Ubuntu:
# https://www.patricksoftwareblog.com/steps-for-starting-a-new-flask-project-using-python3/
# flask run --port 1337 --no-debugger --host=0.0.0.0

@app.route("/")
def index():
    return render_template('index.html', param="a parameter")  # im templates Ordner


@app.route("/hello")
def hello():
    return "Hello World"


@app.route("/hello/<int:zahl>")  # Eingabe einer Zahl nach /hello/
def quadrat(zahl):
    return "Das Quadrat ist " + str(zahl * zahl)  # Umwandlung in String


# dynamisch URLs generieren
@app.route("/dynamisch")
def url():
    return '<a href=' + url_for("name", name="Micha") + '>Sei gegrüßt</a>'


@app.route("/name/<string:name>")
def name(name):
    return "Hello " + name + "!"


@app.route("/login", methods=['POST', 'GET'])
def login():
    cookie = request.cookies.get('username')
    if cookie is not None:
        return "Hallo " + cookie + " (aus Cookie ausgelesen)"
    if request.method == 'POST':
        name1 = request.form['name']
    else:
        name1 = request.args.get('name')
    resp = make_response("Hello " + name1 + "!")
    resp.set_cookie('username', name1)
    return resp


folder = "C:/Users/micha/Dropbox/HP Laptop/Python/PycharmProjects/UdemyTutorialFlask"
extensions = set(['txt', 'jpg', 'png'])


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            return redirect(request.url)
    return '''
        <h1>Upload</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        '''


@app.route("/session", methods=['GET', 'POST'])
def sessions(): # Name wird jetzt in session auf der Serverseite gespeichert, nicht in Cookies
    # print(request.cookies) # Ausgabe des Cookie
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(request.url)
    else:
        if 'name' in session:
            return "Hallo " + escape(session['name'])
        else:
            return '''
            <form method="post">
                <p><input type=text name=name>
                <p><input type=submit value=Login>
            </form>
            '''


@app.route("/logout")
def logout():
    session.pop('name', None)
    return redirect(url_for('sessions'))


app.secret_key = "\xdd\xa536\x81\x9c\xd9]gl;@\xcd\xfaPx\xaa!\xdb$\x03\x1a\xf7\x06"

if __name__ == '__main__':
    app.run(port=1337, debug=True)  # vor Veröffentlichen debug=false setzen
