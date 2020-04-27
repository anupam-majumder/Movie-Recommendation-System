from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import mysql.connector
from recommender import Predictor
from recommender import rating_updater
from datetime import datetime

app = Flask(__name__)

__port = 12394
__host = '0.0.0.0'
__database = 'movies'
__localhost = 'localhost'
__user = 'root'
__password = '12345678'
__table = 'MovieURL'


connection = mysql.connector.connect(host=__localhost,database=__database,user=__user,password=__password)

@app.route('/')
def home():
    print("Movie recommendsation system is on!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        movie_lists = {}
        movie_lists["recommends"] = __get_movies(["Toy Story (1995)","GoldenEye (1995)","Four Rooms (1995)"])
        movie_lists["userid"] =  request.data
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})
   
@app.route('/getRecommendations', methods=['GET', 'POST'])
def get_recommendations():
    error = None
    if request.method == 'POST':
        #method call for prediction
        userid = request.data.decode('utf-8')
        predict_movies = Predictor.Predict_movies()
        recommendations = predict_movies.predict(userid)
        #get movie url from db
        movies = []
        genre = []
        for movie in recommendations:
            for name,gnr in movie.items():
                movies.append(name)
                genre.append(gnr)
        movie_lists = {}
        movie_lists["recommends"] = __get_movies(movies)
        for i in range(len(genre)):
            movie_lists["recommends"][i]["genre"] = genre[i]
        movie_lists["userid"] =  request.data
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})


@app.route('/getSeen', methods=['GET', 'POST'])
def get_seen():
    error = None
    if request.method == 'POST':
        #method call for prediction
        userid = request.data.decode('utf-8')
        seen_prediction_obj = Predictor.Seen_movies()
        seen_movies = seen_prediction_obj.seen(userid)
        #get movie url from db
        movies = []
        genre = []
        for movie in seen_movies:
            for name,gnr in movie.items():
                movies.append(name)
                genre.append(gnr)
        movie_lists = {}
        movie_lists["recommends"] = __get_movies(movies)
        for i in range(len(genre)):
            movie_lists["recommends"][i]["genre"] = genre[i]
        movie_lists["userid"] =  request.data
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})


@app.route('/getRating', methods=['GET', 'POST'])
def get_rating():
    error = None
    if request.method == 'POST':
        #method call for prediction
        userid = request.data.decode('utf-8')
        #get movie url from db
        movies = []
        genre = []
        movie_lists = {}
        movie_lists["recommends"] = __get_movies_to_rate()
        for i in range(len(genre)):
            movie_lists["recommends"][i]["genre"] = genre[i]
        movie_lists["userid"] =  request.data
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})

@app.route('/setRating', methods=['GET', 'POST'])
def set_rating():
    error = None
    if request.method == 'POST':
        #method call for prediction
        request_data = request.data.decode('utf-8')
        request_data = json.loads(request_data)
        new_ratings = []
        print(request_data)
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        for req in request_data:
            if "rating" not in req:
                continue
            if req["rating"] == "0":
                continue
            temp_tup = []
            temp_tup.append(req["userid"])
            temp_tup.append(req["id"])
            temp_tup.append(int(req["rating"]))
            temp_tup.append(int(timestamp))
            new_ratings.append(tuple(temp_tup))
        print(new_ratings)
        #rating_updater(new_ratings)
        return json.dumps({"success":True})

    else:
        return json.dumps({"success":True})


def __get_movies_to_rate():
    lst_of_movies = []
    if connection.is_connected():
        sql_select_Query = "select ID,Name,Poster from "+__table+" limit 12;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for record in records:
            movie_obj = {}
            movie_obj["id"] =  record[0]
            movie_obj["movie"] = record[1]
            movie_obj["url"] = record[2]
            lst_of_movies.append(movie_obj)
    return lst_of_movies #[{'movie':'movie_name','url','url2'}]

def __get_movies(predicted):
    lst_of_movies = []
    if connection.is_connected():
        for movie in predicted:
            sql_select_Query = "select ID,Name,Poster from "+__table+" where ID="+movie+";"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            movie_obj = {}
            movie_obj["id"] = records[0][0]
            movie_obj["movie"] = records[0][1]
            movie_obj["url"] = records[0][2]
            lst_of_movies.append(movie_obj)
    return lst_of_movies #[{'movie':'movie_name','url','url2'}]
    

if __name__ == '__main__':
    save_prediction_obj = Predictor.Save_Predictions()
    save_prediction_obj.generate_predictions()
    app.run(host=__host, port=__port, debug=True)

