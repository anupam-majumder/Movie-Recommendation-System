#!/usr/bin/env python
import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd
from datetime import datetime
import os
from os.path import dirname, abspath
import itertools
import math
from random import random
import pickle

ml_100k_path = "../../../ml-100k/"


class Save_Predictions:
    def __init__(self):
        self.movie_dict = dict()
        self.watched_movies = dict()
        self.seen_by_user = dict()
        self.pred_for_user = dict()
        
        self.predictions_path = ml_100k_path+"predictions.npz"
        self.data_file_path = ml_100k_path+"u.data"
        self.item_file_path = ml_100k_path+"u.item"
        self.output_file_seen=ml_100k_path+"Movies_seen_by_user"
        self.output_file_predict=ml_100k_path+"Movies_suggested_for_user"
    
    def make_seen_pred_dicts(self,user_movie_dict):
        for k in user_movie_dict :
            mov = user_movie_dict[k]

            for i in mov:
                movie_id = i[1]
                if movie_id not in self.watched_movies[k]:
                    m_predict = self.movie_dict[movie_id]
                    try :
                        self.pred_for_user[k].append(m_predict)
                    except KeyError :
                        self.pred_for_user[k] = list()
                        self.pred_for_user[k].append(m_predict)                    
                else:
                    m_seen = self.movie_dict[movie_id]
                    try :
                        self.seen_by_user[k].append(m_seen)
                    except KeyError :
                        self.seen_by_user[k] = list()
                        self.seen_by_user[k].append(m_seen)
   
    def parse_line(self,line):
        line = line.split("\t")
        uid, iid, r, timestamp = (line[i].strip() for i in range(4))
        return uid, iid, float(r), timestamp

    def Read_Data(self,data_file_path,shuffle=True):
        with open(os.path.expanduser(data_file_path)) as item_file_path:
            raw_ratings = [self.parse_line(line) for line in itertools.islice(item_file_path, 0, None)]
        if shuffle:
            np.random.seed(73)
            np.random.shuffle(raw_ratings)

        raw_len = len(raw_ratings)
        train = raw_ratings[:math.ceil(raw_len*0.8)]
        test = raw_ratings[math.ceil(raw_len*0.8):]
        for i in train :
            try :
                self.watched_movies[i[0]].append(i[1])
            except KeyError :
                self.watched_movies[i[0]] = list()
                self.watched_movies[i[0]].append(i[1])


    def Read_Data_pipe(self,data_file_path,shuffle=True) :
        with open(os.path.expanduser(data_file_path), errors='ignore') as item_file_path:
            raw_ratings = [self.parse_line_pipe(line) for line in itertools.islice(item_file_path, 0, None)]
        for i in range(len(raw_ratings)):
            self.movie_dict[raw_ratings[i][0]] = raw_ratings[i][1:]
        return raw_ratings


    def parse_line_pipe(self,line):
        line = line.split("|")
        return line
    
    def make_user_movie_dict(self,users_list, movies_list, ratings_list):
        user_movie = dict()
        for i in range(len(users_list)):
            temp = [ratings_list[i],movies_list[i]]
            try :
                user_movie[users_list[i]].append(temp)
                user_movie[users_list[i]].sort(reverse=True)
            except KeyError :
                user_movie[users_list[i]] = list()
                user_movie[users_list[i]].append(temp)
        return user_movie
    
    def generate_predictions(self):
        npzfile = np.load(self.predictions_path)

        user = npzfile['arr_0'].tolist()
        item = npzfile['arr_1'].tolist()
        rating = npzfile['arr_2'].tolist()
        
        user_movie = self.make_user_movie_dict(user, item, rating)	
        self.Read_Data(self.data_file_path,True)
        mdata = self.Read_Data_pipe(self.item_file_path)
        
        self.make_seen_pred_dicts(user_movie)
        
        self.dict_to_pickle(self.seen_by_user,self.output_file_seen)
        self.dict_to_pickle(self.pred_for_user, self.output_file_predict)
    
    def dict_to_pickle(self,dictionary, pickle_file):
        with open(pickle_file+".pickle", 'wb') as handle:
            pickle.dump(dictionary, handle)

class Predict_movies:
    def __init__(self):
        self.pred_path=ml_100k_path+"Movies_suggested_for_user"
        self.pred_dict=dict()
        self.genre = [ 'Action ',' Adventure ',' Animation ','Childrens ',' Comedy ',' Crime ',' Documentary ',' Drama ',' Fantasy ',
              'Film-Noir ',' Horror ',' Musical ',' Mystery ',' Romance ',' Sci-Fi ','Thriller ',' War ',' Western ']
    def unpickle(self, pickle_file):
        with open(pickle_file+".pickle", 'rb') as handle:
            self.pred_dict = pickle.load(handle)
        
    def predict(self,usr):
        self.unpickle(self.pred_path)
        
        pred_movie_str_list = []
        for j in self.pred_dict[usr]:
            movie_str={}
            movie_str[j[0]]=[]
            for it in range(5,23):
                if j[it].strip()=='1':
                    movie_str[j[0]].append(self.genre[it-5])
            pred_movie_str_list.append(movie_str)
            
        return pred_movie_str_list

class Seen_movies:
    def __init__(self):
        self.seen_path=ml_100k_path+"Movies_seen_by_user"
        self.seen_dict=dict()
        self.genre = [ 'Action ',' Adventure ',' Animation ','Childrens ',' Comedy ',' Crime ',' Documentary ',' Drama ',' Fantasy ',
              'Film-Noir ',' Horror ',' Musical ',' Mystery ',' Romance ',' Sci-Fi ','Thriller ',' War ',' Western ']
    
    def unpickle(self, pickle_file):
        with open(pickle_file+".pickle", 'rb') as handle:
            self.seen_dict = pickle.load(handle)
        
    def seen(self,usr):
        self.unpickle(self.seen_path)
        
        seen_movie_str_list = []
        for j in self.seen_dict[usr]:
            movie_str={}
            movie_str[j[0]]=[]
            for it in range(5,23):
                if j[it].strip()=='1':
                    movie_str[j[0]].append(self.genre[it-5])
            seen_movie_str_list.append(movie_str)
            
        return seen_movie_str_list
