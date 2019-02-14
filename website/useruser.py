import numpy as np

def similarity(matrix):
    product = np.dot(matrix, matrix.T)
    diagonal = np.sqrt(np.diagonal(product)).reshape(1,-1)
    return product / diagonal / diagonal.T

def useruser_predict(user, ratings, k=40):
    cosine = similarity(ratings)
    movies = ratings.shape[1]
    predictions = np.zeros(movies)
    friends = cosine[-1].argsort()[-(k+1):-1]
    for i in range(movies):
    	if ratings[-1,i] == 0:
        	predictions[i] = np.sum(ratings[:,i][friends] * cosine[-1][friends]) / np.sum(np.abs(cosine[-1][friends]))
    return predictions