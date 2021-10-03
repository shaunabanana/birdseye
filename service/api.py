import numpy as np
from flask import Flask
from flask_restful import Resource, Api
from hdbscan import HDBSCAN
from scipy.cluster.hierarchy import fcluster


app = Flask(__name__)
api = Api(app)

class Cluster(Resource):

    def get(self):
        return {'hello': 'world'}

api.add_resource(Cluster, '/cluster')

if __name__ == '__main__':
    app.run(debug=True)