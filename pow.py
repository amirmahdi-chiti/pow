import hashlib 
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import jsonpickle
import threading

class Block: 
    def __init__(self, data, previous_hash, nonce, timestamp, hash): 
        """ 
        Initializes a new Block object with  
        the given data and previous hash. 
        """
        self.data = data 
        self.previous_hash = previous_hash 
        self.nonce = nonce
        self.timestamp =  timestamp
        self.hash = hash
  
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
    
 



    
  
class Blockchain:

    def __init__(self, difficulty): 
        """ 
        Initializes a new Blockchain object with  
        a genesis block. 
        """
        self.difficulty = difficulty
        self.index = 0
        self.chain = [self.create_genesis_block()] 
  
    def create_genesis_block(self): 
        """ 
        Creates the first block of the blockchain with  
        arbitrary data and a previous hash of "0". 
        """
        temp = Block("Genesis Block", "0", nonce= 0 ,timestamp= str(datetime.datetime.now()) , hash="")
        temp.hash = temp.calculate_hash()
        return temp

  
    def add_block(self, new_block): 
        """ 
        Adds a new block to the blockchain with  
        the given data. 
        """
        new_block.previous_hash = self.chain[-1].hash
          
        # Difficulty level of 4 
        new_block.mine_block(self.difficulty)   
        self.chain.append(new_block)
        self.index += 1
    
    def check_valid_block(self,block: Block):
        return (block.previous_hash == self.chain[-1].hash) and (block.calculate_hash() == block.hash) 
  
# create a new blockchain 
app = Flask(__name__)
blockchain = Blockchain(4)
# Create a lock
lock = threading.Lock()

@app.route('/')
def home():
    return 'Proof Of Work ...! Author:Amirmahdi Chiti   -    Iman Jalali     -     Seyed Mohammad Asadi'


@app.route('/add_block', methods=['POST'])
def add_block():
    lock.acquire()
    try:
        # Retrieve JSON-pickled block from the request
        # Deserialize using jsonpickle

        json_data = request.get_json()

    # Create an instance of MyClass from the JSON data
        block = Block(**json_data)

        if not blockchain.check_valid_block(block):
            return jsonify({'message': 'Failed'}), 200
        
        blockchain.add_block(block)
        response = {'data': block.data,
                    'index': blockchain.index,
                    'timestamp': block.timestamp,
                    'nonce': block.nonce,
                    'previous_hash': block.previous_hash,
                    'hash': block.hash}
    finally:
        lock.release()
    return jsonify(response), 200



@app.route('/get_chain', methods=['GET'])
def get_chain():
        print(blockchain.chain)
        response = {'chain': jsonpickle.dumps(blockchain.chain, unpicklable=False),
                    'length': len(blockchain.chain)}
        return jsonify(response), 200


@app.route('/hash_lastblock', methods=['GET'])
def hash_lastblock():
    return blockchain.chain[-1].hash


app.run(host='127.0.0.1', port=5000)