import pandas as pd

def getIds():
	# reading csvs
	linksdf = pd.read_csv('ml-latest-small/links.csv', index_col='movieId', dtype={'imdbId':str, 'tmdbId':str})
	moviesdf = pd.read_csv('ml-latest-small/movies.csv', index_col='movieId')
	df = pd.concat([moviesdf, linksdf], axis=1)
	df = df.iloc[::-1]

	# gettings imdb ids
	movieIds = {}
	movieGenres = df['genres'].tolist()

	for i in range(len(movieGenres)):
	    genre = movieGenres[i].split('|')[0]
	    if genre in movieIds:
	        if len(movieIds[genre]) < 15:
	            movieIds[genre].append(df.iloc[i]['imdbId'])
	    else:
	        movieIds[genre] = [df.iloc[i]['imdbId']]

	del movieIds['(no genres listed)']
	return movieIds

if __name__=="__main__":
	movieIds = getIds()