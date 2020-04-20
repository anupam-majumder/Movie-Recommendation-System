from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print("hi this is here")
    print(request.data)
    if request.method == 'POST':
        print("hi this is inside post")
        return request.data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
