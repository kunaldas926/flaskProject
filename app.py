# app.py

import os

import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_TABLE = os.environ['dynamodbTest']
client = boto3.client('dynamodb')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/employee/<string:employeeId>")
def get_user(employeeId):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': employeeId}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'employeeId': item.get('employeeId').get('S'),
        'firstName': item.get('firstName').get('S'),
        'lastName': item.get('lastName').get('S'),
        'email': item.get('firstName').get('S')
    })


@app.route("/employee", methods=["POST"])
def create_user():
    # employeeId = request.json.get('employeeId')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    email = request.json.get('email')
    # if not employeeId or not firstName or not lastName or not email:
    if not firstName or not lastName or not email:
        return jsonify({'error': 'Please provide details'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'firstName': {'S': firstName},
            'lastName': {'S': lastName},
            'email': {'S': email}
        }
    )

    return jsonify({
        'firstName': firstName,
        'lastName': lastName,
        'email': email
    })


if __name__ == '__main__':
    app.run()
