import hashlib
import json
import time
from datetime import datetime
from Day1_Blockchain import Block
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    
    
    def create_genesis_block(self):
        return Block(0, datetime.now(), {"message": "Genesis Block"}, "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def mine_block(self,difficulty):
     self.hash=self.calculate_hash()
     target="0" * difficulty
     start_time = time.time()
     while self.hash[:difficulty] != target:
        self.nonce +=1
        self.hash=self.calculate_hash()
     if self.nonce % 10000 == 0:
            print(f"Trying nonce: {self.nonce}")
     end_time=time.time()
     print(f"Block mined! Nonce: {self.nonce}, Time: {end_time - start_time:.2f}s")

     print(f"Block mined: {self.hash}")
    
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if the hash is still valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
    
    

# Test the blockchain
my_blockchain = Blockchain()
my_blockchain.add_block(Block(1, datetime.now(), {"amount": 100}, ""))
my_blockchain.add_block(Block(2, datetime.now(), {"amount": 200}, ""))

print(f"Is blockchain valid? {my_blockchain.is_chain_valid()}")

# Try to tamper with the blockchain
my_blockchain.chain[1].data = {"amount": 1000}
print(f"After tampering, is blockchain valid? {my_blockchain.is_chain_valid()}")