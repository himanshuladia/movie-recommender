# Movie Recommender Web Application

## How To Use The Webapp

The webapp homepage consists of a number of movies from different genres and release years. The user has to first register
and login into the application. The homepage is then updated to provide option to rate each movie on a scale of 1-5. The user
is required to rate **atleast 10** movies across different genres and click on the submit button. After pressing the submit button, the 3 algorithms take data and calculate predictions *(note that this will take some time since the existing database is large to generate better predictions)*. Once the processing is done, the user is shown recommendations sorted according to different algorithms.

![homepage_with_login](https://github.com/himanshuladia/movie-recommender/blob/master/screenshots/homepage_with_login.png)

## Approach Followed

Used collaborative filtering methods to predict movie ratings for a user -

1. In general itemitem collaborative filtering worked better than useruser collaborative filtering, irrespective of the similarity
function used. This is possibly because itemitem collaborative filtering is more resistant towards user bias. Comparing the
similarity functions, it was observed the plain, cosine similarity tends to work better than correlation for sparse matrices.
 Tried using centered cosine, but it fails when users rate all the movies same, so dropped it. The value of nearest neighbor was
 chosen such that the mse loss is minimized.
 
2. Matrix factorization outperforms both of the above methods in terms of mean squared error loss. Using appropriate random
initialization, a single iteration of stochastic gradient descent was able to give the best results. With some trial and error
K=40 was chosen for latent features for the embeddings. When a new user arrives, the algorithm is trained for a single
iteration, and the user and item embeddings are multiplied to get the predictions.

## Codebase and Directory Structure

### Python Files

* **selection.py** - Uses movielens development dataset to select imdbIds of movies of different genres and release years.

* **scrape.py** - Uses Beautiful Soup and Requests library to extract imdbId, name, releaseYear, thumbnail, rating, summary and
duration of selected movies from imdb's official website.

* **insert_movies.py** - Uses pymongo to insert the "movies" collection into the mongodb database. The "movies" collection consists
the data of the scraped movies.

* **insert_ratings.py** - Uses pymongo to insert the "ratings" collection into the mongodb database. It consists of ratings of
actual users and is used as dummy data to train the models.

### Jupyter Notebooks

* **Collaborative Filtering.ipynb** - This notebook explores user-user and item-item collaborative filtering methods. The root mean
squared accuracy is used to test the models and pick the best value of nearest neighbours.

* **Matrix Factorization.ipynb** - This notebook explored the matrix factorization method using stochastic gradient implemented with
pure numpy code for vectorized and fast results.

### Web Application

* **Dump folder** - Consists of mongodb database dump, with 3 collections in total. Namely, movies, ratings, and users.

* **Static folder** - Consists of all the css, javascript and fonts used to make the web application

* **Templates folder** -
1. layout.html - Contains the basic layout of the webapp, including navbar, header, footer.
2. index.html - Extends layout, It is the homepage of the webapp, shows all the movies in the database, sorted by genres.
3. login.html - Extends layout, It is the login system of the webapp.
4. register.html - Extends layout, It is the register system of the webapp.
5. recommendations.html - Extends layout, It gives the recommendation to the user.

* **app.py** - Uses flask framework as the backend for the webapp

* **useruser.py** - Provides useruser_predict function to the main app.py module

* **itemitem.py** - Provides itemitem_predict function to the main app.py module

* **matrixfactorization.py** - Provides matrixfactorization_predict function to the main app.py module

### Data

* **ml-latest-small** - MovieLens development dataset, small in size
* **database.csv** - User-item ratings matrix made from the movielens dataset

## Dependencies Used

1. Flask - for backend
2. Jinja2 - for HTML templating
3. Passlib - for hashing user passwords
4. Numpy - for fast numerical computation
5. Pandas - for manipulating csvs
6. Sklearn - for loss metrics
7. Pymongo - for communicating with mongodb

## Deployment

The application is deployed using digital ocean's droplet and is available to use on the ip address [68.183.81.208](http://68.183.81.208), as long as I can manage the free credits :)
