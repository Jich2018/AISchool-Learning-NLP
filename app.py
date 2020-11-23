from dao.cosmos_manager import Cosmos_Manager
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__, instance_relative_config=False, template_folder='./flaskr/templates')

app.config.from_pyfile('./config.py')

@app.route('/')
def index():
    cosmos_manager = Cosmos_Manager()
    result = cosmos_manager.get({"database": "movie-reco", "container": "asin", "query": "SELECT * FROM c"})
    return render_template('index.html', movies = result)

@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    cosmos_manager = Cosmos_Manager()
    query = f"SELECT * FROM asin c where c.asin='{str(movie_id).zfill(10)}'"
    result = cosmos_manager.get({"database": "movie-reco", "container": "asin", "query": query})
    reviews = cosmos_manager.get({"database": "movie-reco", "container": "reviews", "query": "SELECT * FROM reviews c"})
    return render_template('movie.html', movie=result, reviews=reviews)

@app.route('/user/<user_id>/movies')
def movies(user_id):
    cosmos_manager = Cosmos_Manager()
    query_arguments = request.args

    #default is for recommendation
    query = f"SELECT * FROM recommendations c where c.reviewer='{user_id}'"
    result = cosmos_manager.get({"database": "movie-reco-lstm", "container": "recommendations", "query": query})

    if "cat" in query_arguments:
        if query_arguments["cat"] == "viewed":
            #TODO:
            result = None
        elif query_arguments["cat"] == "reviewed":
            #TODO:
            result = None

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=6789, debug=True)
    