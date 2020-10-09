# AISchool-Learning-NLP

## How to use this repo

Python > 3.7,  
pip > 20.2.0,  
virtualenv (install by 'python -m pip virtualenv')

1. create a virtual environment 'virtualenv venv'
2. activate the venv '.\venv\Script\activate.bat'
3. restore the dependency 'python -m pip install -r requirements.txt'
4. download necessary corpus  
python -m nltk.downloader averaged_perceptron_tagger  
python -m nltk.downloader punkt  
python -m nltk.downloader treebank  

python app.py will start a web server on localhost:6789
flask run will start a web server on localhost:5000
