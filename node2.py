import hashlib 
import datetime
import hashlib
import json
from flask import Flask, jsonify 
import jsonpickle
import threading
import requests
import jsonpickle


class Block: 
    def __init__(self, data, previous_hash): 
        """ 
        Initializes a new Block object with  
        the given data and previous hash. 
        """
        self.data = data 
        self.previous_hash = previous_hash 
        self.nonce = 0
        self.timestamp =  str(datetime.datetime.now())
        self.hash = self.calculate_hash() 
  
    def calculate_hash(self): 
        """ 
        Calculates the SHA-256 hash of the  
        block's data, previous hash, and nonce. 
        """
        sha = hashlib.sha256() 
        sha.update(str(self.data).encode('utf-8') + 
                   str(self.previous_hash).encode('utf-8') + 
                   str(self.nonce).encode('utf-8') + 
                   str(self.timestamp).encode('utf-8')) 
                   
        return sha.hexdigest() 
  
    def mine_block(self, difficulty): 
        """ 
        Mines the block using the Proof-of-Work algorithm  
        with the given difficulty level. 
        """
        while self.hash[0:difficulty] != "0" * difficulty: 
            self.nonce += 1
            self.hash = self.calculate_hash() 
  
        print("Block mined:", self.hash)


class Node:
    def __init__(self, username) -> None:
        self.username = username
        self.reward = 0


app = Flask(__name__)
node = Node("Node2")
@app.route('/mine_block', methods=['GET'])
def mine():
    hash_lastblock = requests.get("http://127.0.0.1:5000/hash_lastblock").text
    block = Block("Transaction data", hash_lastblock)
    block.mine_block(4)
    json_data = json.dumps(block.__dict__)
    # Set the headers for JSON data
    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://127.0.0.1:5000/add_block", data=json_data, headers=headers)
    node.reward += 1
    return response.text, 200

@app.route('/reward', methods=['GET'])
def reward():
    return str(node.reward)

app.run(host='127.0.0.1', port=5002)