from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import mysql.connector
from recommender import Predictor


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
    print(request.data)
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
    print(request.data)
    if request.method == 'POST':
        #method call for prediction
        userid = request.data.decode('utf-8')
        predict_movies = Predictor.Predict_movies()
        recommendations = predict_movies.predict(userid)#[{"Toy Story (1995)":["horror","romance"]},{"GoldenEye (1995)":["action","comedy"]},{"Four Rooms (1995)":["action","comedy"]}] #get_predicted_movies(userid)
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
    print(request.data)
    if request.method == 'POST':
        #method call for prediction
        userid = request.data.decode('utf-8')
        seen_prediction_obj = Predictor.Seen_movies()
        seen_movies = seen_prediction_obj.seen(userid)#[{"Four Rooms (1995)":["action","comedy"]},{"Toy Story (1995)":["horror","romance"]},{"GoldenEye (1995)":["action","comedy"]}] #get_seen_movies(userid)
        #get movie url from db
        print(seen_movies)
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
    print(request.data)
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
        print(movie_lists)
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})

def __get_movies_to_rate():
    lst_of_movies = []
    if connection.is_connected():
        sql_select_Query = "select Name,Poster from "+__table+" limit 12;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for record in records:
            movie_obj = {}
            movie_obj["movie"] = record[0]
            movie_obj["url"] = record[1]
            lst_of_movies.append(movie_obj)
    return lst_of_movies #[{'movie':'movie_name','url','url2'}]

def __get_movies(predicted):
    lst_of_movies = []
    if connection.is_connected():
        print(predicted)
        for movie in predicted:
            sql_select_Query = "select Name,Poster from "+__table+" where ID="+movie+";"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            print("records = ",records[0][0])
            print("records = ",records[0][1])
            movie_obj = {}
            movie_obj["movie"] = records[0][0]
            movie_obj["url"] = records[0][1]
            lst_of_movies.append(movie_obj)
    return lst_of_movies #[{'movie':'movie_name','url','url2'}]

if __name__ == '__main__':
    save_prediction_obj = Predictor.Save_Predictions()
    save_prediction_obj.generate_predictions()
    app.run(host=__host, port=__port, debug=True)

