import numpy as np
from scipy.sparse import csr_matrix
import tools as tl
import pandas as pd
from datetime import datetime
import os
import itertools
import math



class model :

	def __init__(self, train_sparse):

		self.n_factors = 20
		self.matrix = train_sparse
		matrix_csc = train_sparse.tocsc()
		self.user_num = matrix_csc.shape[0]
		self.item_num = matrix_csc.shape[1]

		#global mean
		self.global_mean = np.sum(matrix_csc.data) / matrix_csc.size

		#user bias
		self.user_bias = np.zeros(self.user_num, np.double)

		#item bias
		self.item_bias = np.zeros(self.item_num, np.double)

		#user factor
		self.user_factor = np.zeros((self.user_num, self.n_factors), np.double) + .1

		#item factor
		self.item_factor = np.zeros((self.item_num, self.n_factors), np.double) + .1

		#item preference facotor
		self.item_preference = np.zeros((self.item_num, self.n_factors), np.double) + .1

		#weights for neihbourhood
		self.weights = np.zeros((self.item_num,self.item_num))

		#implicit feedback
		self.implicit_feedback = np.zeros((self.item_num,self.item_num))


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

	def predict(self, u, i):
	
		Nu = self.get_user(u)[0]

		I_Nu = len(Nu)
		sqrt_N_u = np.sqrt(I_Nu)

		y_u = np.sum(self.item_preference[Nu], axis=0) / sqrt_N_u

		w_ij = np.dot((self.get_user(u)[1] - self.global_mean - self.user_bias[u] - self.item_bias[Nu]) ,self.weights[i][Nu])
		c_ij = np.sum(self.implicit_feedback[i,Nu] , axis = 0)
		c_w =  (c_ij + w_ij )/sqrt_N_u


		est = self.global_mean + self.user_bias[u] + self.item_bias[i] + np.dot(self.item_factor[i], self.user_factor[u] + y_u) + c_w
		return est


	def _estimate(self,test, measures, train_dataset,uid_dict,iid_dict):
		# global uid_dict,iid_dict

		users_mean = self.get_user_means()
		items_mean = self.get_item_means()

		raw_test_dataset = test
		# global_mean = np.sum(train_dataset.data) / train_dataset.size


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
			    real, est = r, self.predict(u, i,)
			    alg_count += 1

			est = min(5, est)
			est = max(1, est)
			errors.append(real - est)

		return errors


	def estimate(self,test, measures, train_sparse,uid_dict,iid_dict):
		error = self._estimate(test, measures, train_sparse,uid_dict,iid_dict)
		error = np.sqrt(np.mean(np.power(error, 2)))
		return error


	def train(self,train_sparse,test, n_epochs,uid_dict,iid_dict) :

		n_lr = 0.001
		lr = 0.007
		reg = 0.001
		n_reg = 0.015

		reg7 = 0.005

		for current_epoch in range(n_epochs):
		    start = datetime.now()
		    print(" processing epoch {}".format(current_epoch))
		    
		    for u,i,r in self.all_ratings():
		        
		        Nu = self.get_user(u)[0]
		        I_Nu = len(Nu)
		        sqrt_N_u = np.sqrt(I_Nu)

		        
		        item_preference_u = np.sum(self.item_preference[Nu], axis=0)

		        u_impl_prf = item_preference_u / sqrt_N_u

		        c_ij = np.sum(self.implicit_feedback[i,Nu] , axis = 0)

		        w_ij = np.dot((self.get_user(u)[1] - self.global_mean - self.user_bias[u] - self.item_bias[Nu]) ,self.weights[i][Nu])


		        c_w =  (c_ij + w_ij )/sqrt_N_u

		       
		        rp = self.global_mean + self.user_bias[u] + self.item_bias[i] + np.dot(self.item_factor[i], self.user_factor[u] + u_impl_prf) + c_w

		        
		        e_ui = r - rp

		        #sgd
		        self.user_bias[u] += lr * (e_ui - reg7 * self.user_bias[u])
		        self.item_bias[i] += lr * (e_ui - reg7 * self.item_bias[i])
		        self.user_factor[u] += lr * (e_ui * self.item_factor[i] - reg * self.user_factor[u])
		        self.item_factor[i] += lr * (e_ui * (self.user_factor[u] + u_impl_prf) - reg * self.item_factor[i])
		        for j in Nu:
		            self.item_preference[j] += lr * (e_ui * self.item_factor[j] / sqrt_N_u - reg * self.item_preference[j])
		        for j in Nu :
		            self.weights[i,j] += n_lr * (e_ui/ sqrt_N_u * (r - self.global_mean - self.user_bias[u] - self.item_bias[j]) - n_reg * self.weights[i,j])
		        for j in Nu :
		            self.implicit_feedback[i,j] += n_lr * ((e_ui / sqrt_N_u) - n_reg * self.implicit_feedback[i,j])


		    n_lr *= 0.9
		    lr *= 0.9
		    print("Time For Epoch :: "+str(datetime.now()-start))
		    # start = datetime.now()
		    print("Err = ",self.estimate(test,"rmse",train_sparse,uid_dict,iid_dict))
		    print("Time For Error :: "+str(datetime.now()-start))

file_name = "../ml-100k/u.data"

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

A = model(train_dataset)
print(A.train(train_dataset,test_dataset,20,uid_dict,iid_dict))

