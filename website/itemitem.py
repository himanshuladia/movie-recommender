import numpy as np

def similarity(matrix):
    product = np.dot(matrix, matrix.T)
    diagonal = np.sqrt(np.diagonal(product)).reshape(1,-1)
    return product / diagonal / diagonal.T

def itemitem_predict(user, ratings, k=40):
    ratings = ratings.T
    cosine = similarity(ratings)
    movies = ratings.shape[0]
    predictions = np.zeros(movies)
    for i in range(movies):
        friends = cosine[i].argsort()[-(k+1):-1]
        if ratings[i,-1] == 0:
        	predictions[i] = np.sum(ratings[:,-1][friends] * cosine[i][friends]) / np.sum(np.abs(cosine[i][friends]))
    return predictions