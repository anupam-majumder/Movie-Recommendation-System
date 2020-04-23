import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd
from datetime import datetime
import os
from os.path import dirname, abspath
import itertools
import math

current_file_path = abspath(__file__)
ml_100k_path = current_file_path
for i in range(4):
	ml_100k_path = dirname(ml_100k_path)
ml_100k_path += "/ml-100k/"

file_name = ml_100k_path+"/u.data"

def mapping(train) :
    uid_dict = {}
    iid_dict = {}
    current_u_index = 0
    current_i_index = 0

    row = []
    col = []
    data = []

    for urid,irid,r,timestamp in train :

        try:
            uid = uid_dict[urid]
        except KeyError:
            uid = current_u_index
            uid_dict[urid] = current_u_index
            current_u_index += 1
        try:
            iid = iid_dict[irid]
        except KeyError:
            iid = current_i_index
            iid_dict[irid] = current_i_index
            current_i_index += 1

        row.append(uid)
        col.append(iid)
        data.append(r)

    train_sparse = csr_matrix((data, (row, col)))
    return train_sparse, uid_dict, iid_dict

def parse_line(line):
    line = line.split("\t")
    uid, iid, r, timestamp = (line[i].strip() for i in range(4))
    return uid, iid, float(r), timestamp

def Read_Data(file_name,shuffle=True) :

    # data = pd.read_csv(file_name,sep = "\t", names = ["uid","iid","r","timst"])
    # data.sort_values(by = "timst", inplace = True)

    # train = data.head(n = int(0.8 * data.shape[0]))
    # test = data.drop(train.index)
    with open(os.path.expanduser(file_name)) as f:
        raw_ratings = [parse_line(line) for line in itertools.islice(f, 0, None)]
    if shuffle:
        # train_test shuffle in reproducable manner
        np.random.seed(400)
        np.random.shuffle(raw_ratings)

    raw_len = len(raw_ratings)

    train_sparse,uid,iid = mapping(raw_ratings[:math.ceil(raw_len*0.8)])
    test = raw_ratings[math.ceil(raw_len*0.8):]
    return train_sparse,uid,iid,test


def all_ratings(matrix,axis=1):

    coo_matrix = matrix.tocoo()

    if axis == 1:
        return zip(coo_matrix.row, coo_matrix.col, coo_matrix.data)
    else:
        return coo_matrix.row, coo_matrix.col, coo_matrix.data

def get_user(matrix, u):

    ratings = matrix.getrow(u).tocoo()
    return ratings.col, ratings.data

def get_item(matrix, i):
    ratings = matrix.getcol(i).tocoo()
    return ratings.row, ratings.data

def get_item_means(matrix):
   
    item_means = {}
    for i in np.unique(matrix.tocoo().col) :
        item_means[i] = np.mean(get_item(matrix,i)[1])
    return item_means

def get_user_means(matrix):
  
    users_mean = {}
    for u in np.unique(matrix.tocoo().row) :
        users_mean[u] = np.mean(get_user(matrix,u)[1])
    return users_mean



def train(train_sparse,test, n_epochs = 30, n_factors = 20) :

    matrix = train_sparse.tocsc()
    user_num = matrix.shape[0]
    item_num = matrix.shape[1]

    global_mean = np.sum(matrix.data) / matrix.size
    user_bias = np.zeros(user_num, np.double)
    item_bias = np.zeros(item_num, np.double)
    user_factor = np.zeros((user_num, n_factors), np.double) + .1
    item_factor = np.zeros((item_num, n_factors), np.double) + .1
    item_pref_factor = np.zeros((item_num, n_factors), np.double) + .1
    neighbouhood_weights = np.zeros((item_num,item_num))
    implicit_feedback = np.zeros((item_num,item_num))

    n_lr = 0.001
    lr = 0.007
    reg = 0.001
    n_reg = 0.015

    reg7 = 0.005

    for current_epoch in range(n_epochs):
        start = datetime.now()
        print(" processing epoch {}".format(current_epoch))
        
        for u,i,r in all_ratings(matrix):
            
            Nu = get_user(matrix,u)[0]
            I_Nu = len(Nu)
            sqrt_N_u = np.sqrt(I_Nu)

            
            y_u = np.sum(item_pref_factor[Nu], axis=0)

            u_impl_prf = y_u / sqrt_N_u

            c_ij = np.sum(implicit_feedback[i,Nu] , axis = 0)

            w_ij = np.dot((get_user(matrix,u)[1] - global_mean - user_bias[u] - item_bias[Nu]) ,neighbouhood_weights[i][Nu])


            c_w =  (c_ij + w_ij )/sqrt_N_u

           
            rp = global_mean + user_bias[u] + item_bias[i] + np.dot(item_factor[i], user_factor[u] + u_impl_prf) + c_w

            
            e_ui = r - rp

            #sgd

            user_bias[u] += lr * (e_ui - reg7 * user_bias[u])
            item_bias[i] += lr * (e_ui - reg7 * item_bias[i])
            user_factor[u] += lr * (e_ui * item_factor[i] - reg * user_factor[u])
            item_factor[i] += lr * (e_ui * (user_factor[u] + u_impl_prf) - reg * item_factor[i])
            for j in Nu:
                item_pref_factor[j] += lr * (e_ui * item_factor[j] / sqrt_N_u - reg * item_pref_factor[j])
            for j in Nu :
                neighbouhood_weights[i,j] += n_lr * (e_ui/ sqrt_N_u * (r - global_mean - user_bias[u] - item_bias[j]) - n_reg * neighbouhood_weights[i,j])
            for j in Nu :
                implicit_feedback[i,j] += n_lr * ((e_ui / sqrt_N_u) - n_reg * implicit_feedback[i,j])




        n_lr *= 0.9
        lr *= 0.9
        print("Time For Epoch :: "+str(datetime.now()-start))
     
    return user_bias,item_bias,item_pref_factor,implicit_feedback,neighbouhood_weights,item_factor,user_factor,global_mean

train_dataset, uid_dict, iid_dict, test_dataset = Read_Data(file_name,True)
user_bias,item_bias,item_pref_factor,implicit_feedback,neighbouhood_weights,item_factor,user_factor,global_mean = train(train_dataset,test_dataset,30)
np.savez("../integrated_model",user_bias,item_bias,item_pref_factor,implicit_feedback,neighbouhood_weights,item_factor,user_factor,global_mean)