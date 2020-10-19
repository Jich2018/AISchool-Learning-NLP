from flask import Flask, render_template

app = Flask(__name__)

mymovies = [{'id':1, 'title':'Titanic', 'description':'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.', 'year':'1997', 'genres':'Drama,Romance'},
        {'id':2, 'title':'Rush Hour','description':'A loyal and dedicated Hong Kong Inspector teams up with a reckless and loudmouthed L.A.P.D. detective to rescue the Chinese Consul kidnapped daughter, while trying to arrest a dangerous crime lord along the way.', 'year':'1998', 'genres': 'action, comedy, crime, thriller'}]

@app.route('/')
def index():
    return render_template('index.html', movies=mymovies) 

def get_movie(movie_id):
    movie = mymovies[movie_id-1]
    return movie 

@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = get_movie(movie_id)
    return render_template('movie.html', movie=movie)
