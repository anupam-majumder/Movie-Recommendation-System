import numpy as np
from scipy.sparse import csr_matrix
import os
from os.path import dirname, abspath
import pandas as pd
from datetime import datetime
import os
import itertools
import math



class Predictor :

	def __init__(self, train_sparse):
		self.matrix = train_sparse

		npzfile = np.load(ml_100k_path+"integrated_model.npz")

		self.user_bias 			= npzfile['arr_0']
		self.item_bias 			= npzfile['arr_1']
		self.item_preference  	= npzfile['arr_2']
		self.implicit_feedback  = npzfile['arr_3']
		self.weights  			= npzfile['arr_4']
		self.item_factor  		= npzfile['arr_5']
		self.user_factor        = npzfile['arr_6']
		self.global_mean 		= npzfile['arr_7']

		self.user_raw = list()
		self.item_raw = list()
		self.i_rating = list()


	def all_ratings(self,axis=1):
	    coo_matrix = self.matrix.tocoo()
	    if axis == 1:
	        return zip(coo_matrix.row, coo_matrix.col, coo_matrix.data)
	    else:
	        return coo_matrix.row, coo_matrix.col, coo_matrix.data

	def get_user(self, u):
	    ratings = self.matrix.getrow(u).tocoo()
	    return ratings.col, ratings.data

	def get_item(self, i):
	    
	    ratings = self.matrix.getcol(i).tocoo()
	    return ratings.row, ratings.data


	def get_item_means(self):
	    item_means = {}
	    for i in np.unique(self.matrix.tocoo().col) :
	        item_means[i] = np.mean(self.get_item(i)[1])
	    return item_means

	def get_user_means(self):
	    users_mean = {}
	    for u in np.unique(self.matrix.tocoo().row) :
	        users_mean[u] = np.mean(self.get_user(u)[1])
	    return users_mean


	def convert_id(self,u,i,r,itemID_dict, userID_dict):
		self.user_raw.append(list(userID_dict.keys())[list(userID_dict.values()).index(u)])
		self.item_raw.append(list(itemID_dict.keys())[list(itemID_dict.values()).index(i)])
		self.i_rating.append(r)

	def predict(self, u, i,iid_dict,uid_dict):
	
		Nu = self.get_user(u)[0]

		I_Nu = len(Nu)
		sqrt_N_u = np.sqrt(I_Nu)

		y_u = np.sum(self.item_preference[Nu], axis=0) / sqrt_N_u

		w_ij = np.dot((self.get_user(u)[1] - self.global_mean - self.user_bias[u] - self.item_bias[Nu]) ,self.weights[i][Nu])
		c_ij = np.sum(self.implicit_feedback[i,Nu] , axis = 0)
		c_w =  (c_ij + w_ij )/sqrt_N_u

		est = self.global_mean + self.user_bias[u] + self.item_bias[i] + np.dot(self.item_factor[i], self.user_factor[u] + y_u) + c_w
		temp = min(5, est)
		temp = max(1, est)
		self.convert_id(u,i,temp,iid_dict,uid_dict)
		return est


	def _estimate(self,test, measures, train_dataset,uid_dict,iid_dict):

		users_mean = self.get_user_means()
		items_mean = self.get_item_means()

		raw_test_dataset = test

		all = len(raw_test_dataset)
		errors = []
		cur = 0
		alg_count = 0

		for raw_u, raw_i, r, _ in raw_test_dataset:
			cur += 1
			has_raw_u = raw_u in uid_dict
			has_raw_i = raw_i in iid_dict

			if not has_raw_u and not has_raw_i:
			    real, est = r, self.global_mean
			elif not has_raw_u:
			    i = iid_dict[raw_i]
			    real, est = r, items_mean[i]
			elif not has_raw_i:
			    u = uid_dict[raw_u]
			    real, est = r, users_mean[u]
			else:
			    u = uid_dict[raw_u]
			    i = iid_dict[raw_i]
			    real, est = r, self.predict(u, i,iid_dict,uid_dict)
			    alg_count += 1

			est = min(5, est)
			est = max(1, est)
			errors.append(real - est)

		return errors


	def estimate(self,test, measures, train_sparse,uid_dict,iid_dict):
		error = self._estimate(test, measures, train_sparse,uid_dict,iid_dict)
		error = np.sqrt(np.mean(np.power(error, 2)))
		return error


current_file_path = abspath(__file__)
ml_100k_path = current_file_path
for i in range(4):
	ml_100k_path = dirname(ml_100k_path)
ml_100k_path += "/ml-100k/"

file_name = ml_100k_path+"u.data"


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

	with open(os.path.expanduser(file_name)) as f:
		raw_ratings = [parse_line(line) for line in itertools.islice(f, 0, None)]
	if shuffle:
		np.random.shuffle(raw_ratings)

	raw_len = len(raw_ratings)
	train_sparse,uid,iid = mapping(raw_ratings[:int(math.ceil(raw_len*0.8))])
	test = raw_ratings[int(math.ceil(raw_len*0.8)):]

	return train_sparse,uid,iid,test




train_dataset, uid_dict, iid_dict, test_dataset = Read_Data(file_name,True)

predicts = Predictor(train_dataset)
np.savez(ml_100k_path+"predictions",np.array(predicts.user_raw),np.array(predicts.item_raw),np.array(predicts.i_rating))




