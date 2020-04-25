from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import mysql.connector
#from recommender import predictor.py 
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
    train_model()
    print("Movie recommendsation system is on!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print(request.data)
    if request.method == 'POST':
        movie_lists = {}
        movie_lists["recommends"] = __get_movies(["Toy Story (1995)","GoldenEye (1995)","Four Rooms (1995)"])
        movie_lists["userid"] =  request.data
        print(movie_lists)
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})
   
@app.route('/getRecommendations', methods=['GET', 'POST'])
def get_recommendations():
    error = None
    print(request.data)
    if request.method == 'POST':
        #method call for prediction
        userid = request.data
        recommendations = [{"Toy Story (1995)":["horror","romance"]},{"GoldenEye (1995)":["action","comedy"]},{"Four Rooms (1995)":["action","comedy"]}] #get_predicted_movies(userid)
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
        print(movie_lists)
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})


@app.route('/getSeen', methods=['GET', 'POST'])
def get_seen():
    error = None
    print(request.data)
    if request.method == 'POST':
        #method call for prediction
        userid = request.data
        seen_movies = [{"Four Rooms (1995)":["action","comedy"]},{"Toy Story (1995)":["horror","romance"]},{"GoldenEye (1995)":["action","comedy"]}] #get_seen_movies(userid)
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
        print(movie_lists)
        return json.dumps(movie_lists)

    else:
        return json.dumps({"success":True})


def __get_movies(predicted):
    lst_of_movies = []
    if connection.is_connected():
        for movie in predicted:
            sql_select_Query = "select Poster from "+__table+" where Name="+"'"+movie+"';"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            movie_obj = {}
            movie_obj["movie"] = movie
            movie_obj["url"] = records[0]
            lst_of_movies.append(movie_obj)
    return lst_of_movies #[{'movie':'movie_name','url','url2'}]

if __name__ == '__main__':
    app.run(host=__host, port=__port, debug=True)

