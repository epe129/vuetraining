from flask import Flask, request,jsonify,json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/rekisteröidy", methods=["POST","GET"])
def rekisteröidy():
    if request.method == "POST":
        post_data = request.get_json()
        name   = post_data.get('name'),
        password  = post_data.get('password')
        print(name)
        print(password)
    return jsonify("response_object")

@app.route("/kirjaudu", methods=["POST","GET"])
def kirjaudu():
    if request.method == "POST":
        post_data = request.get_json()
        name   = post_data.get('name'),
        password  = post_data.get('password')
        print(name)
        print(password)
    return jsonify("response_object")

if __name__ == '__main__':    
   app.run()