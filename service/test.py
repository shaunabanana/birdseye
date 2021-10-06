import json
from requests import put


with open('../dataset/data/index.json') as f:
    data = f.read()
    response = put('http://localhost/cluster/3', data=data)
    print(response.text)

    tweets = json.loads(data)
    labels = json.loads(response.text)
    for i, tweet in enumerate(tweets):
        tweet['cluster'] = labels[i]
    response = put('http://localhost/keyword/', data=json.dumps(tweets))
    print(response.text)
    