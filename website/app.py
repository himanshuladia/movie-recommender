from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymongo
import numpy as np
from passlib.hash import sha256_crypt
from functools import wraps
import json
from useruser import useruser_predict
from itemitem import itemitem_predict
from matrixfactorization import matrixfactorization_predict

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["imdb"]
moviesCollection = db["movies"]
usersCollection = db["users"]
ratingsCollection = db["ratings"]

app = Flask(__name__)

@app.route('/')
def home():
	movies = moviesCollection.find()
	a = request.cookies.get('stars')

	return render_template("index.html", movies=movies)

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login_page'))
	return wrap

def rating_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if len(json.loads(request.cookies.get('stars'))) < 10:
			flash("Please select atleast 10 movies!")
			return redirect(url_for('home'))
		else:
			return f(*args, **kwargs)
	return wrap

@app.route("/logout/")
@login_required
def logout():
	session.clear()
	return redirect(url_for('home'))

@app.route('/login/', methods=['GET','POST'])
def login_page():
	error = ''
	if request.method == "POST":
		attempted_email = request.form['email']
		attempted_password = request.form['password']
		if usersCollection.find_one({'email':attempted_email}) is None:
			error = "Email doesn't exists, register first!"
		elif sha256_crypt.verify(attempted_password, usersCollection.find_one({'email':attempted_email})['password']):
			session['logged_in'] = True
			session['email'] = attempted_email
			return redirect(url_for('home'))
		else:
			error = "Invalid credentials, try again!"
	return render_template("login.html", error=error, title='Login')

@app.route('/register/', methods=['GET','POST'])
def register_page():
	error = ''
	if request.method == "POST":
		email = request.form['email']
		password = sha256_crypt.encrypt(str(request.form['password']))
		if usersCollection.find_one({'email':email}) is None:
			usersCollection.insert_one({'email':email, 'password':password})
			session['logged_in'] = True
			session['email'] = email
			return redirect(url_for('home'))
		else:
			error="Email id already exists!"
	return render_template("register.html", error=error, title='Register')

@app.route('/recommendations/')
@rating_required
def submit_ratings():
	allImdbIds, userImdbIds, userRatings, database = getUserData(json.loads(request.cookies.get('stars')))
	webImdbIds = getWebImdbIds()
	
	# User User
	useruserPredictions = useruser_predict(userRatings, database)
	useruserResult = getResult(useruserPredictions, allImdbIds, webImdbIds, userImdbIds)

	# Item Item
	itemitemPredictions = itemitem_predict(userRatings, database)
	itemitemResult = getResult(itemitemPredictions, allImdbIds, webImdbIds, userImdbIds)

	# Matrix Factorization
	matrixfactorizationPredictions = matrixfactorization_predict(userRatings, database)
	matrixfactorizationResult = getResult(matrixfactorizationPredictions, allImdbIds, webImdbIds, userImdbIds)

	movies = moviesCollection.find()
	return render_template("recommendations.html", useruserIds=useruserResult[:10], itemitemIds=itemitemResult[:10], matrixfactorizationIds=matrixfactorizationResult[:10], movies=movies)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")

# Utility Functions
def getIdsRatings(cookie):
	tempUser = ratingsCollection.find_one()
	myUser = {}
	for key in tempUser:
		if key!='_id':
			if key in cookie:
				cookie[key] = float(cookie[key])
				myUser[key] = cookie[key]
			else:
				myUser[key] = 0.0
	return list(myUser.keys()), list(cookie.keys()), list(myUser.values())

def getUserData(cookie):
	allImdbIds, userImdbIds, userRatings = getIdsRatings(cookie)

	database = []
	ratings = ratingsCollection.find()
	for rating in ratings:
		database.append(list(rating.values())[1:])
	database.append(userRatings)

	allImdbIds = np.array(allImdbIds)
	userImdbIds = np.array(userImdbIds)
	userRatings = np.array(userRatings)
	database = np.array(database)

	return allImdbIds, userImdbIds, userRatings, database

def getWebImdbIds():
	movies = moviesCollection.find()
	webImdbIds = []
	for movie in movies:
		webImdbIds.append(movie['imdbId'])
	return webImdbIds

def getResult(predictions, allImdbIds, webImdbIds, userImdbIds):
	allImdbIds = allImdbIds[predictions.argsort()[::-1]]
	result = []
	for imdbId in allImdbIds:
		if imdbId in webImdbIds and imdbId not in userImdbIds:
			result.append(imdbId)
	return result

if __name__=="__main__":
	app.secret_key = '123123123'
	app.run(debug=True)