import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import json
import config
import uuid
from dao.cosmos_manager import Cosmos_Manager

m = Cosmos_Manager(config.NLP_COSMOS_ENDPOINT, config.NLP_COSMOS_KEY)

def sync_reco():
    with open('.\\recommender\\top3recommendations.json') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            datum = json.loads(line)
            print("Line {}: {}".format(cnt, line.strip()))
            sync(datum)
            line = fp.readline()
            cnt += 1

def sync(datum):
    datum['id'] = uuid.uuid1().hex[:6].lower()
    cosmos_datum = {'database': 'movie-reco', 'container': 'recommendations', 'value': datum}
    m.add(cosmos_datum)

if __name__ == "__main__":
    sync_reco()
