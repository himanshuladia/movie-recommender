from bs4 import BeautifulSoup
import requests

def scrapeMovie(url):
	# get the imdbID
	imdbId = url.split('/')[-2][2:]

	# request to main webpage
	response = requests.get(url)
	source = response.text
	soup = BeautifulSoup(source, 'lxml')

	title = soup.find('div', class_='title_wrapper')
	name = title.h1.text[:-8]
	year = title.h1.a.text

	time = title.find('div', class_='subtext').time.text.strip()

	genres = title.find('div', class_='subtext').find_all('a')
	genres.pop()
	for i in range(len(genres)):
		genres[i] = genres[i].text

	poster = soup.find('div', class_='poster').a.img['src']

	rating = soup.find('div', class_='ratingValue').span.text

	# request to plot webpage
	response = requests.get(url+'plotsummary')
	source = response.text
	soup = BeautifulSoup(source, 'lxml')

	summary = soup.find('ul', id='plot-summaries-content').li.p.text

	# Create and return dictionary
	json = {'imdbId':imdbId, 'title':name, 'releaseYear':year, 'thumbnail':poster, 'imdbRating':rating, 'synopsis':summary, 'duration':time, 'genres':genres}

	return json

if __name__=="__main__":
	# print(scrapeMovie("https://www.imdb.com/title/tt8108164/"))
	# scrapeMovie("https://www.imdb.com/title/tt0468569/")
	print("https://www.imdb.com/title/tt0468569/".split('/')[-2][2:])


