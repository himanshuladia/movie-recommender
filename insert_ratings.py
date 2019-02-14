import pymongo
import pandas as pd

if __name__=="__main__":
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["imdb"]
	ratings = db['ratings']

	database = pd.read_csv('database.csv')

	ratings.insert_many(database.to_dict('records'))
