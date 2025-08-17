import hashlib
import json
from textwrap import dedent
from time import time

from urllib.parse import urlparse
import requests


from flask import Flask, jsonify, request
from uuid import uuid4

class Blockchain(object):
    # constructor
    
    
    def __init__(self):
        # create an empty list which will store the blockchain and transactions
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        
        # Create a genesis block to start a chain of blockchain
        self.new_block(proof = 100, previous_hash = 1 )
        
        
    def valid_chain(self, chain):
        # this will check whether given Blockchain is valid or not
        # chain <list> : list of blocks of that blockchain
        # return <bool>
        
        last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            print(f"{last_block}")
            print(f"{block}")
            print("\n------------\n")
            
            # Check the hash of block is correct
            if self.hash(last_block) != block['previous_hash']:
                return False
            
            # Check proof of block is correct pp' must have 4 leading 0's
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
              
        return True
    
    def resolve_conflict(self):
        # This function will contain our consenses Algorithm and 
        # It resolves conflict by replacing our chain with the longest one
        neighbours = self.nodes
        new_chain = None
        
        max_length = len(self.chain)
        # Now verify the chain from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                # if the length is longer than the chain then it is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
                           
        if new_chain:
            self.chain = new_chain
            return True
        return False
                
    
    
        
        
        
    def register_node(self, address):
        """ Add a new node to the list of nodes
        address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """       
        parsed_url = urlparse(address)
        # this will add neighbouring node to our network
        self.nodes.add(parsed_url.netloc)
        
        
    def proof_of_work(self, last_proof):
        """ Simplest Proof of Work Algorithm
        - Find a number p such that (pp') has the hash of 4 leading 0's
        - Where p is the previous proof and p' is the proof of new proof
        
        last_proof <int> 
        return proof : <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof
    
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
        
        
    def new_block(self, proof, previous_hash = None):
        """ This function is used to create a new block in block
        
        proof <int> : The proof is obtain by the Proof of work Algorithm
        previous_hash (Optional)<str> : It contain the hash of previous block
        return <dict> : new block
        
        """
        block = {
            'index' : len(self.chain) + 1 ,
            'timestamp' : time(),
            'transaction' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),  
        }   
        
        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block 
   
   
   
    def new_transaction(self, sender, recipient, amount):
        """ adds a new transaction to go into the new mined block

        Args:
            sender (str): Address of Sender
            recipient (str): Address of receiver
            amount (int): Amount
            return <int>: The index of that block which will hold this transaction
        """
        self.current_transactions.append(
            {
                'sender' : sender,
                'recipient' : recipient,
                'amount' : amount,
            }
        )
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        """ Creates a SHA-256 hash of block
        
        block <dict> : Block
        return <str> : 
        
        """
        # we must make sure that dictionary is ordered OR we'll have inconsistent hashes
        
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
        
            
    @property
    def last_block(self):
        # it defines the last block of chain
        return self.chain[-1]
    





# Initiate a node 
app  = Flask(__name__)

# Generate a unique address for node
node_identifier = str(uuid4()).replace('-','')

# Initiate the BlockChain\
blockchain = Blockchain()

@app.route("/mine", methods = ["GET"])
def mine():
    # We will run the PoW to add proof of next block
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof  = blockchain.proof_of_work(last_proof)
    
    # We must receive a reward for finding a proof of next block 
    # The sender "0" shows that this person mined a new coin
    
    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1
        
    )    
    
    # forge a new block and add it into the blockchain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,  previous_hash)
    
    response = {
        'message' : 'New Block Forge',
        'index' : block['index'],
        'transaction' : block['transaction'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash'],
    }
    
    return jsonify(response), 200
    
    
@app.route("/transactions/new", methods = ["POST"])
def new_transaction():
    values = request.get_json()
    
    # verifying that user has given all data of sender, receiver, amount
    required = ['sender', 'recipient', 'amount']
    if not all(key in values for key in required):
        return "Missing requirement ", 400
    
    # If the values data is verified then add a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = f"Message : your Transaction is being added to block of index {index}"
    
    return jsonify(response), 201



@app.route("/chain", methods = ["GET"])
def chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain),
    }
    return jsonify(response),200


@app.route("/nodes/register", methods = ['POST', 'GET'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    
    if nodes is None:
        return "Please return a valid list of nodes", 400
    
    for node in nodes:
        blockchain.register_node(node)
        
    response = {
        'message' : 'New node has been Added',
        'total_nodes' : len(blockchain.nodes)
    }
    
    return jsonify(response), 201

@app.route("/nodes/resolve", methods = ['GET'])
def consenses():
    replaced = blockchain.resolve_conflict()
    if replaced:
        response = {
            'message' : 'Our chain is replaced ',
            'new_chain' : blockchain.chain,
        }
    
    else:
       response = {
            'message' : 'Our chain is Authoritative',
            'chain' : blockchain.chain,
        } 
       
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
