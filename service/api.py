from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

import json
import numpy as np
import pandas as pd
from hdbscan import HDBSCAN
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import fcluster

from sklearn.feature_extraction.text import CountVectorizer
from ctfidf import CTFIDFVectorizer


app = Flask(__name__)
CORS(app)

api = Api(app)


class Cluster(Resource):

    def put(self, clusters):
        result = {}

        # Parse the data into a large vector
        tweets = json.loads(request.data)
        # print(tweets)
        vectors = []
        for tweet in tweets:
            vectors.append(tweet['vector'])
        X = np.array(vectors)
        print(X)

        # Calculate clustering
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(X)
        labels = kmeans.labels_.tolist()
        # clusterer = HDBSCAN(min_cluster_size=10)
        # clusterer.fit(X)

        # # Get the number of cluster required
        # Z = clusterer.single_linkage_tree_.to_numpy()
        # labels = fcluster(Z, clusters, criterion='maxclust')
        # print(labels)
        # print(labels.shape)

        return kmeans.labels_.tolist()


class Keyword(Resource):

    def put(self):
        result = {}

        # Parse the data into a large vector
        tweets = json.loads(request.data)
        labels = [tweet['cluster'] for tweet in tweets]
        print(labels)

        # Load stopwords
        with open('./stopwords.txt') as f:
            stopwords = f.readlines()
            stopwords = [word.replace('\n', '') for word in stopwords]

        # print(tweets[0])
        # Filter sentences using stopwords
        sentences = [tweet['parsed'] for tweet in tweets]
        filtered = []
        for sentence in sentences:
            sentence = sentence.lower().split(' ')
            sentence = [word for word in sentence if word not in stopwords]
            filtered.append(' '.join(sentence))

        docs = pd.DataFrame({'Document': filtered, 'Class': labels})
        docs_per_class = docs.groupby(['Class'], as_index=False).agg({'Document': ' '.join})

        # Create bag of words
        count_vectorizer = CountVectorizer().fit(docs_per_class.Document)
        count = count_vectorizer.transform(docs_per_class.Document)
        words = count_vectorizer.get_feature_names()

        # Calculate cTFIDF
        ctfidf = CTFIDFVectorizer().fit_transform(count, n_samples=len(docs)).toarray()

        # Sort words by cTFIDF
        label_index = [label for label in docs_per_class.Class]
        for label in docs_per_class.Class:
            print(label)
            result[label] = []
            order = list(ctfidf[label_index.index(label)].argsort())
            order.reverse()
            for index in order:
                result[label].append(words[index])

        # Filter out words that are the same for 
        # set_list = [set(result[label]) for label in result]
        # intersection = set.intersection(*set_list)
        # print(intersection)
        # for label in docs_per_class.Class:
        #     for other_label in docs_per_class.Class:
        #         if label == other_label:
        #             continue
        #         this_set = set(result[label])
        #         other_set = set(result[label])

        counter = 0
        while counter < 4:
            removed = False
            for label in result:
                others = [l for l in result if label != l ]
                word = result[label][counter]
                print(word)
                
                hit = False
                for other in others:
                    if word in result[other][:4]:
                        hit = True
                        break
                if hit or ('19' in word) or ('corona' in word) or ('covid' in word) or ('vaccin' in word):
                    for label in result:
                        print('Removing', word)
                        result[label].remove(word)
                        removed = True
            
            if not removed:
                counter += 1
            
            set_list = [set(result[label][:4]) for label in result]
            intersection = set.intersection(*set_list)
            if len(intersection) == 0:
                found = False
                for label in result:
                    for word in result[label][:4]:
                        if '19' in word or 'corona' in word or 'covid' in word or 'vaccine' in word:
                            found = True
                if not found:
                    break

        for label in result:
            result[label] = result[label][:4]
        return result

api.add_resource(Cluster, '/cluster/<int:clusters>')
api.add_resource(Keyword, '/keyword/')

if __name__ == '__main__':
    app.run(debug=True)