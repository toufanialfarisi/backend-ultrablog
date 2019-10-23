import requests
from flask import jsonify, json

url = "http://localhost/"
payload = {"judul": "coba yang ini", "konten": "ini", "featureImage": "imageimage"}
data = requests.post(url=url, json=payload)
print(data)
