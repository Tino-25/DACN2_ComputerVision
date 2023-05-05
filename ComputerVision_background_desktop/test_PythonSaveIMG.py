import requests
url = "http://127.0.0.1:8000/static/image/preProcessing/red-car.png"
response = requests.get(url)
with open("image.jpg", "wb") as f:
    f.write(response.content)