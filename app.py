import os

from flask import Flask,render_template
from google.cloud import firestore

db = firestore.Client();

app = Flask(__name__)

GOOGLE_APPLICATION_CREDENTIALS = 'credentials.json'

@app.route('/')
def welcome():
    return "Hello"

@app.route('/<path:path>')
def catch_all(path):
    target = os.environ.get('TARGET', 'World')
    print(path)
    try:
        data = db.collection(u'links').document(path).get()
        data = data.to_dict()
        link = "{}".format(data[u"link"]);
        db.collection(u'links').document(path).update({'views': data[u"views"]+1})
        return render_template('template.html',link=link)
    except Exception as e:
        print(e)
        return "404"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
