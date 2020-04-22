from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print("hi this is here")
    print(request.data)
    if request.method == 'POST':
        print("hi this is inside post")
        return json.dumps({"userid":['url1','url2','url3']})

def __get_movies():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

