#!/usr/bin/env python
from googlesearch import search
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

directory_data = '../../../ml-100k/'
query_list = pd.read_csv(directory_data + 'u.item',sep = '|',encoding="ISO-8859-1",header=None).iloc[:,:2].to_numpy()
db_img =[]
for movie in query_list:
    print(movie[1])
    img_link = []
    img_link.append(movie[1])
    
    for url in search(movie[1]+" "+"imdb", tld="com", num=1, stop=1, pause=2):
        soup = bs(requests.get(url).content, "html.parser")
        img = soup.find("img")
        img_url = img.attrs.get("src")
        img_link.append(img_url)
    db_img.append(np.array(img_link)) 
    
posters = pd.DataFrame(db_img)
posters.columns=['Name','Poster']

cols_genre = ['ID','Name']+list(pd.read_csv(directory_data + 'u.genre',sep='|',header=None).iloc[:,0].to_numpy())
cols = [0,1]+[i for i in range(5,24)]

genre = pd.read_csv(directory_data + 'u.item',encoding="ISO-8859-1",sep='|',header=None).iloc[:,cols]
genre.columns=cols_genre

genre.merge(posters,left_on='Name', right_on='Name').to_csv(directory_data + 'Posters.csv',index=False)
