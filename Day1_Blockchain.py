# Buliding My first Blockchain
import time
import hashlib
import json
from datetime import datetime

class Block:
 def __init__(self,index,timestamp,data,previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.nonce = 0
    self.hash = self.calculate_hash()
    
    
 def calculate_hash(self):
    block_string = json.dumps({
       "index": self.index,
       "timestamp":str(self.timestamp),
       "data":self.data,
       "previous_hash":self.previous_hash,
       "nonce":self.nonce
        
        
        
    },sort_keys=True )
    return hashlib.sha256(block_string.encode()).hexdigest()
 
 def mine_block(self, difficulty):
        target = "0" * difficulty
        start_time = time.time()
        
        print(f"⛏️  Mining block with difficulty {difficulty}...")
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()  # Recalculate hash with new nonce
            
            # Show progress every 100000 attempts
            if self.nonce % 100000 == 0:
                print(f"   Trying nonce: {self.nonce}")
        
        end_time = time.time()
        print(f"✅ Block mined! Nonce: {self.nonce}, Time: {end_time - start_time:.2f}s")
        print(f"   Hash: {self.hash}")

 def __repr__(self):
    return f"Block({self.index},{self.hash[:8]}...)"


#Creating Genesis Block

genesis_block= Block(0,datetime.now(),{"Message":"Genesis Block"},"0")
print(f"Genesis Block: {genesis_block}")
print(f"Hash: {genesis_block.hash}")
    






