import os

from flask import Flask,render_template,request,redirect,url_for
from google.cloud import firestore

db = firestore.Client();

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Hello"

@app.route('/<path:path>')
def catch_all(path):
    try:
        data = db.collection(u'links').document(path).get()
        data = data.to_dict()
        link = "{}".format(data[u"link"]);
        db.collection(u'links').document(path).update({'views': data[u"views"]+1})
        return render_template('redirect.html',links=link)
    except Exception as e:
        print(e)
        return "404"

@app.route('/a', methods=['GET'])
def add_link():
    link=request.args.get('link');
    short=request.args.get('short');
    try:
        db.collection(u'links').document(short).set({u'short': short, u'link': link, u'views': 0})
    except Exception as e:
        print(e)
        return e;
    return redirect(url_for('admin'));


@app.route('/d', methods=['GET'])
def delete_link():
    short=request.args.get('short');
    try:
        db.collection(u'links').document(short).delete()
    except Exception as e:
        print(e)
        return e;
    return redirect(url_for('admin'));

@app.route('/ccdx')
def admin():
    data = db.collection(u'links').get()
    links = [];
    for doc in data:
        links.append(doc.to_dict())
    return render_template('interface.html', links=links)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
