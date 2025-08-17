import hashlib
import json

from time import time
from uuid import uuid4


class Blockchain(object):
    # constructor
    def __init__(self):
        # create an empty list which will store the blockchain and transactions
        self.chain = []
        self.current_transactions = []
        
        # Create a genesis block to start a chain of blockchain
        self.new_block(proof = 100, previous_hash = 1 )
        
        
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
            'previous_hash' : previous_hash if previous_hash == 1 else self.hash(self.chain[-1]),  
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
    
    