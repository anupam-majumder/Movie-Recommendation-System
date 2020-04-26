import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd
from datetime import datetime
import os
import itertools
import math
from random import random


# In[45]:


npzfile = np.load("../predictions.npz")


# In[46]:


user = npzfile['arr_0'].tolist()
item = npzfile['arr_1'].tolist()
rating = npzfile['arr_2'].tolist()


# In[47]:


user_movie = dict()
for i in range(len(user)):
    temp = [rating[i],item[i]]
    try :
        user_movie[user[i]].append(temp)
        user_movie[user[i]].sort(reverse=True)
    except KeyError :
        user_movie[user[i]] = list()
        user_movie[user[i]].append(temp)


# In[48]:


file_name = "../input/u.data"
watched_movies = dict()
def parse_line(line):
    line = line.split("\t")
    uid, iid, r, timestamp = (line[i].strip() for i in range(4))
    return uid, iid, float(r), timestamp

def Read_Data(file_name,shuffle=True) :
    global watched_movies
    with open(os.path.expanduser(file_name)) as f:
        raw_ratings = [parse_line(line) for line in itertools.islice(f, 0, None)]
    if shuffle:
        np.random.seed(73)
        np.random.shuffle(raw_ratings)

    raw_len = len(raw_ratings)
    train = raw_ratings[:int(math.ceil(raw_len*0.8))]
    test = raw_ratings[int(math.ceil(raw_len*0.8)):]
    for i in train :
        try :
            watched_movies[i[0]].append(i[1])
        except KeyError :
            watched_movies[i[0]] = list()
            watched_movies[i[0]].append(i[1])       


# In[49]:


global watched_movies
shuffle = True
with open(os.path.expanduser(file_name)) as f:
    raw_ratings = [parse_line(line) for line in itertools.islice(f, 0, None)]
if shuffle:
    np.random.seed(73)
    np.random.shuffle(raw_ratings)

raw_len = len(raw_ratings)
train = raw_ratings[:int(math.ceil(raw_len*0.8))]
test = raw_ratings[int(math.ceil(raw_len*0.8)):]
for i in train :
    try :
        watched_movies[i[0]].append(i[1])
    except KeyError :
        watched_movies[i[0]] = list()
        watched_movies[i[0]].append(i[1]) 


# In[51]:


Read_Data(file_name,True)


# In[53]:


f = "../input/u.item"
movie_dict = dict()
def Read_Data_pipe(file_name,shuffle=True) :
    global movie_dict
    global watched_movies
    with open(os.path.expanduser(file_name)) as f:
        raw_ratings = [parse_line_pipe(line) for line in itertools.islice(f, 0, None)]
    for i in range(len(raw_ratings)):
        movie_dict[raw_ratings[i][0]] = raw_ratings[i][1:]
    return raw_ratings
def parse_line_pipe(line):
    line = line.split("|")
    return line
mdata = Read_Data_pipe(f)


# In[54]:


seen_by_user = dict()
pred_for_user = dict()
for k in user_movie :
    mov = user_movie[k]
    for i in mov:
        ele = i[1]
        if ele not in watched_movies[k]:
            m_predict = movie_dict[ele]
            try :
                pred_for_user[k].append(m_predict)
            except KeyError :
                pred_for_user[k] = list()
                pred_for_user[k].append(m_predict)                    
        else:
            m_seen = movie_dict[ele]
            try :
                seen_by_user[k].append(m_seen)
            except KeyError :
                seen_by_user[k] = list()
                seen_by_user[k].append(m_seen)


# In[57]:


genre = [ 'Action ',' Adventure ',' Animation ','Childrens ',' Comedy ',' Crime ',' Documentary ',' Drama ',' Fantasy ',
              'Film-Noir ',' Horror ',' Musical ',' Mystery ',' Romance ',' Sci-Fi ','Thriller ',' War ',' Western ']


# In[58]:


ii=7


# In[59]:


i = 0
j=5
# i is the item(movie) and j is the corresponding entry for that movie


# In[60]:


#take any user
usr = '23'
seen_movie_str_list = []
for j in seen_by_user[usr]:
    movie_str = j[0]+"::"
    for it in range(5,23):
        if j[it].strip()=='1':
            movie_str = movie_str+' '+genre[it-5]
    seen_movie_str_list.append(movie_str)
pred_movie_str_list = []
for j in pred_for_user[usr]:
    movie_str = j[0]+"::"
    for it in range(5,23):
        if j[it].strip()=='1':
            movie_str = movie_str+' '+genre[it-5]
    pred_movie_str_list.append(movie_str)


# In[61]:


print("Watched movies by user: "+usr)
for i in seen_movie_str_list:
    print(i)


# In[62]:


print("Predicted movies for user: "+usr)
count = 10
c = 0
for i in pred_movie_str_list:
    c= c+1
    if(c>10):
        break
    print(i)

