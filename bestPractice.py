from flask import Flask, request, jsonify, Response
from OpenSSL import SSL    # pip install pyopenssl
import werkzeug
import json
from functools import wraps

from werkzeug.exceptions import abort

app = Flask(__name__)

jsonStore = None

# ***** SSL (Zertifikat nötig) *****
# context = SSL.Context(SSL.TLSv1_2_METHOD)
# context.use_certificate('mycert.crt')
# context.use_privatekey('myprivatekey.key')
# ssl_context=context muss noch in app.run


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")  # bei unbekannten URLs wird immer hierher umgeleitet
def bonus1(path):
    return "Hello World"


# ***** Errorhandling *******
@app.errorhandler(werkzeug.exceptions.NotFound)
def notfound(e):
    return jsonify(error=str(e), myKey="myValue", liste=[2,4,45]), e.code # Fehler als JSON zurückgeben


# ***** Logging *****
@app.route("/logging")
def bonus2():
    app.logger.info("Das ist ein Log")
    return "Hello World"


# ***** JSON empfangen *****
@app.route("/json", methods=['POST'])
def bonus3():
    global jsonStore
    jsonStore = json.loads(request.data.decode('utf-8'))
    print("JSON empfangen:")
    print(jsonStore)
    return ""


# ***** Ausgabe der JSON *****
@app.route("/jsonvar")
def getJsonVar():
    return jsonStore


# ***** Login Fenster *****
def check(username, password):
    return username == "admin" and password == "hjkl"  # bei Verwendung von Passwörtern: SSL benutzen


def auth():
    return Response('Please login!', 401, {'WWW-Authenticate': 'Basic real="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        autho = request.authorization  # nachschauen, ob Authorisierungsparameter im Request sind
        if not autho or not check(autho.username, autho.password):  # oder username/password sind falsch
            return auth()
        return f(*args, **kwargs)
    return decorator


@app.route('/admin')
@requires_auth  # die Funktion admin wird gewrappt, wird requires_auth als f übergeben
def admin():
    return 'hello admin'


if __name__ == '__main__':
    app.run(port=1337, debug=True)

