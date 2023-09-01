from flask import Flask, render_template,request,redirect,url_for,session
import db,string,random,os
from datetime import timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

if __name__ == '__main__':
    app.run(debug=True)