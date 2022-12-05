from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json, pymongo, re
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

client = MongoClient('mongodb://172.17.0.2:27017/')
@app.route('/scores', methods=['POST', 'GET'])
@cross_origin()
def controller():
    req = request.data
    if request.method == 'POST':
        return post()
    elif request.method == 'GET':
        return get(req)
    else:
        return "Method not allowed"
def post():
    req = request.data
    try:
        parsed_req = json.loads(req)
        print(parsed_req)
    except ValueError as e:
        return {"Error!":"Requested information is not a valid json string"}
    db = client[parsed_req['email']]['scores']
    #print(parsed_req)
    
    if 'hit' in parsed_req and 'miss' in parsed_req and 'attempts' in parsed_req:
        print("!!!!!!")
        insert_obj = {"date": datetime.now().isoformat(),"hit":parsed_req['hit'],"miss":parsed_req['miss'],"attempts":parsed_req['attempts']}
        print(parsed_req['email'])
        print(insert_obj)
        print(datetime.now().isoformat())
        post_id = db.insert_one(insert_obj).inserted_id
        post_id
    return_json = str(list(db.find().limit(1).sort("$natural", -1)))
    format_json = json.loads(str(re.sub(r'ObjectId\(\'.*\'\)',"'1'", return_json)).replace("\'",'"'))
    print(format_json)

    return format_json
def get(req):
    #req = request.data
    try:
        parsed_req = json.loads(req)
        print(parsed_req)
    except ValueError as e:
        print(request.data)
        return {"Error!":"Requested information is not a valid json string"}, 400
    db = client[parsed_req['email']]['scores']
    #print( list(db.aggregate( pipeline ) ) )
    return_json = str(list(db.find().limit(1).sort("$natural", -1)))
    format_json = json.loads(str(re.sub(r'ObjectId\(\'.*\'\)',"'1'", return_json)).replace("\'",'"'))
    print(format_json)

    return format_json

app.run(host='172.31.60.5', port=8090)

