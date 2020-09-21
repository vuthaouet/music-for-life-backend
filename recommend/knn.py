import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD

books = pd.read_csv("data.csv")
book_features = pd.concat([books["categories"].str.get_dummies(sep=","), books["author"].str.get_dummies()],axis=1)
min_max_scaler = MinMaxScaler()
book_features = min_max_scaler.fit_transform(book_features)
book_features =  np.round(book_features,2)
print(book_features.shape)
svd = TruncatedSVD(n_components=20)
book_features =  svd.fit_transform(book_features)
nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(book_features)
distances, indices = nbrs.kneighbors(book_features)

def print_similar_books(id):
    result = []
    for i in indices[id][1:]:
        result.append(books["id"][i])
    return result

book_id = 1
# print(print_similar_books(book_id-1))