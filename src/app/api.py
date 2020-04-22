from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    #return render_template('index.html')
    #need to train the model
    print("server is on")

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
        return json.dumps({"recommends":[{"url":"https://images-na.ssl-images-amazon.com/images/M/MV5BNDE0NTQ1NjQzM15BMl5BanBnXkFtZTYwNDI4MDU5..jpg","movie":"movie1"},{"url":"https://images-na.ssl-images-amazon.com/images/M/MV5BNDE0NTQ1NjQzM15BMl5BanBnXkFtZTYwNDI4MDU5..jpg","movie":"movie2"},{"url":"https://images-na.ssl-images-amazon.com/images/M/MV5BNDE0NTQ1NjQzM15BMl5BanBnXkFtZTYwNDI4MDU5..jpg","movie":"movie3"}],"userid":request.data})
    else:
        return json.dumps({"success":True})
    
def __get_movies():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12394, debug=True)

