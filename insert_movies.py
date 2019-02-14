from selection import getIds
from scrape import scrapeMovie
import pymongo
from tqdm import tqdm


if __name__=="__main__":
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["imdb"]
	movies = db["movies"]

	movieIds = getIds()

	# populating the database
	for genre in movieIds.keys():
		imdbIds = movieIds[genre]
		for imdbId in tqdm(imdbIds):
			url = "https://www.imdb.com/title/tt" + imdbId + '/'
			try:
				json = scrapeMovie(url)
				movies.insert_one(json)
			except:
				pass