'''
Define class ReviewsLookup. Get review sentiment by reviewer, or asin.
'''


import json
from collections import Counter
from itertools import islice


class ReviewSentimentLookup:

    def __init__(self):
        self.__reviewer_to_asin_pos = {}
        self.__asin_to_reviewer_pos = {}

        with open("reviewers.json") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    review = json.loads(line)
                    reviewer = review['reviewerID']
                    pos = review['pos']
                    self.__reviewer_to_asin_pos[reviewer] = pos
                except KeyError:
                    continue
                    
        with open("asin.json") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    review = json.loads(line)
                    asin = review['asin']
                    pos = review['pos']
                    self.__asin_to_reviewer_pos[asin] = pos
                except KeyError:
                    continue


    def get_pos_asins_by_reviewer(self, reviewer):
        return self.__reviewer_to_asin_pos[reviewer]


    def get_pos_reviewers_by_asin(self, asin):
        return self.__asin_to_reviewer_pos[asin]


    def gen_recommendation_data(self):
        for reviewer, pos in self.__reviewer_to_asin_pos.items():
            asins = []
            for asin in pos:
                reviewers = self.get_pos_reviewers_by_asin(asin)
                reviewers.remove(reviewer)
                for other in reviewers:
                    asins.extend(self.get_pos_asins_by_reviewer(other))

            counter = Counter(asins)
            counter = {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}

            # remove the reviewed movies of the reviewer
            for asin in pos:
                counter.pop(asin, None)
            counter = dict(islice(counter.items(), 10))

            d = {'reviewer': reviewer, 'recommendation': counter}
            s = json.dumps(d)+"\n"
            name = "recommendations/{}.json".format(reviewer)
            with open(name, 'w') as f:
                f.write(s)


def dump_recommendation(n=5):
    with open("recommendation.json") as f:
        head = [next(f) for x in range(n)]
        print(head)


if __name__ == "__main__":
    lookup = ReviewSentimentLookup()
    #print("get pos asins by reviewer A105C374T9A12")
    #print(lookup.get_pos_asins_by_reviewer("A105C374T9A12"))
    #print("get pos reviewers by asin 0005119367")
    #print(lookup.get_pos_reviewers_by_asin("0005119367"))

    lookup.gen_recommendation_data()
    dump_recommendation(1)