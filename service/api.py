from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

import json
import numpy as np
from hdbscan import HDBSCAN
from scipy.cluster.hierarchy import fcluster


app = Flask(__name__)
CORS(app)

api = Api(app)


class Cluster(Resource):
    def put(self, clusters):
        # Parse the data into a large vector
        tweets = json.loads(request.data)
        print(tweets)
        vectors = []
        for tweet in tweets:
            vectors.append(tweet['vector'])
        X = np.array(vectors)
        print(X)

        # Calculate clustering
        clusterer = HDBSCAN(min_cluster_size=10)
        clusterer.fit(X)

        # Get the number of cluster required
        Z = clusterer.single_linkage_tree_.to_numpy()
        labels = fcluster(Z, clusters, criterion='maxclust')
        print(labels)
        print(labels.shape)
        return labels.tolist()

api.add_resource(Cluster, '/<int:clusters>')

if __name__ == '__main__':
    app.run(debug=True)