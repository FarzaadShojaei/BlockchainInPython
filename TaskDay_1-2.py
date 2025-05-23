import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self,index,timestamp,data,previous_hash,sender,receiver,amount):
        self.index = index
        self.timestamp = str(timestamp)
    
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.sender=sender
        self.receiver=receiver
        self.amount = amount
        self.hash = self.calculate_hash()
        
        
        
    def calculate_hash(self):
     block_string = json.dumps({
       "index": self.index,
       "timestamp":str(self.timestamp),
       "data":self.data,
       "previous_hash":self.previous_hash,
       "nonce":self.nonce,
       "sender":self.sender,
       "receiver":self.receiver,
       "amount":self.amount
    },sort_keys=True)
     return hashlib.sha256(block_string.encode()).hexdigest()
        
    def __repr__(self):
     return f"Block({self.index},{self.hash[:8]}...)"


#Creating Genesis Block

genesis_block= Block(0,datetime.now(),{"Message":"Genesis Block"},"0","Alice","Bob",100)
print(f"Genesis Block: {genesis_block}")
print(f"Hash: {genesis_block.hash}")


Second_block=Block(1,datetime.now(),{"Message":"Second_Block"},genesis_block.hash,"Bob","Charlie",200)
print(f"Genesis Block: {Second_block}")
print(f"Hash: {Second_block.hash}")

Third_block=Block(2,datetime.now(),{"Message":"third_Block"},Second_block.hash,"Charile","Daniel",300)
print(f"Genesis Block: {Third_block}")
print(f"Hash: {Third_block.hash}")

