from requests import put


with open('../dataset/data/index.json') as f:
    data = f.read()
    response = put('http://127.0.0.1/cluster/5', data={'data': data})
    print(response.text)