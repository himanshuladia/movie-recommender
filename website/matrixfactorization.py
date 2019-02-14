import numpy as np

def predict(global_bias, user_bias, item_bias, user_embedding, item_embedding, u, i):
    prediction = global_bias + user_bias[u] + item_bias[i] + np.dot(user_embedding[u],item_embedding[i])
    return prediction

def train(ratings, k=40, learning_rate=0.0001, regularization=0, epochs=1):
    n_users, n_items = ratings.shape
    user_embedding = np.random.normal(scale = 1/k, size=(n_users, k))
    item_embedding = np.random.normal(scale = 1/k, size=(n_items, k))
    global_bias = np.mean(ratings[np.where(ratings != 0)])
    user_bias = np.zeros(n_users)
    item_bias = np.zeros(n_items)
    rows, cols = np.nonzero(ratings)
    for epoch in range(epochs):
        p = np.random.permutation(len(rows))
        rows, cols = rows[p], cols[p]
        for u,i in zip(*(rows,cols)):
            prediction = predict(global_bias, user_bias, item_bias, user_embedding, item_embedding, u, i)
            actual = ratings[u,i]
            e = actual - prediction
            loss = e**2 + regularization*(np.linalg.norm(user_embedding[u]) + np.linalg.norm(item_embedding[i]) + user_bias[u] + item_bias[i])
            user_bias[u] += learning_rate * (e - regularization * user_bias[u])
            item_bias[i] += learning_rate * (e - regularization * item_bias[i])
            user_embedding[u] += learning_rate * (e * item_embedding[i] - regularization * user_embedding[u])
            item_embedding[i] += learning_rate * (e * user_embedding[u] - regularization * item_embedding[i])
    return global_bias, user_bias, item_bias, user_embedding, item_embedding

def matrixfactorization_predict(user, ratings):
	global_bias, user_bias, item_bias, user_embedding, item_embedding = train(ratings)
	predictions = np.dot(user_embedding, item_embedding.T)[-1]
	for i in range(len(user)):
		if user[i] != 0:
			predictions[i] = 0
	return predictions