from dao.cosmos_manager import Cosmos_Manager
from flask import Flask, render_template
import os

app = Flask(__name__, instance_relative_config=False, template_folder='./flaskr/templates')

app.config.from_pyfile('./config.py')

@app.route('/')
def index():
    cosmos_manager = Cosmos_Manager()
    result = cosmos_manager.get({"database": "movie-reco", "container": "reviews", "query": "SELECT * FROM c"})
    return render_template('index.html', data = result[0])

if __name__ == '__main__':
    app.run(port=6789, debug=True)
    