# AISchool-Learning-NLP

## How to use this repo

Prerequisite: 
- Python > 3.7,  
- pip > 20.2.0,  
- virtualenv (install by 'python -m pip virtualenv')

1. create a virtual environment by command 'virtualenv venv'
2. activate the venv '.\venv\Script\activate.bat'
3. restore the dependency 'python -m pip install -r requirements.txt'
4. download necessary corpus  
python -m nltk.downloader averaged_perceptron_tagger  
python -m nltk.downloader punkt  
python -m nltk.downloader treebank  
5. go to Azure, find out the CosmosDB account (nlp-movie-data), copy/paste the cosmos endpoint and cosmos key to the NLP_COSMOS_ENDPOINT and NLP_COSMOS_KEY in config.py. (The running_in_cloud condition is for Azure, to run in local, paste the value in else part)
6. start the service in local by running 'flask run', this will start a web server on localhost:5000. also can start the service by just running 'python app.py', however this will start the web service in a different way as what Azure does, you might see different result or error by starting in this way.


TODO：
the id in the reco matrix is not unique, every update will create a new record. 
integrate with an tool to update the matrix and send signal at an interval. 

