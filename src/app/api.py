from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import mysql.connector

app = Flask(__name__)

__port = 12394
__host = '0.0.0.0'
__database = 'recomendation'
__localhost = 'localhost'
__user = 'root'
__password = '12345678'
__table = 'Movies'


connection = mysql.connector.connect(host=__localhost,database=__database,user=__user,password=__password)

@app.route('/')
def home():
    print("Movie recommendsation system is on!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print(request.data)
    if request.method == 'POST':
        #method call for prediction

        #get movie url from db
        movie_lists = {}
        movie_lists["recommends"] = __get_movies(["mad love","terminator","hulk"])
        movie_lists["userid"] =  request.data

        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})
    
def __get_movies(predicted):
    lst_of_movies = []
    if connection.is_connected():
        for movie in predicted:
            sql_select_Query = "select movie_url from "+__table+" where movie_title="+"'"+movie+"';"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            movie_obj = {}
            movie_obj["movie"] = movie
            movie_obj["url"] = records[0]
            lst_of_movies.append(movie_obj)
    return lst_of_movies

if __name__ == '__main__':
    app.run(host=__host, port=__port, debug=True)

