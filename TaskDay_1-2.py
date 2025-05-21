import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self,index,timestamp,data,previous_hash):
        self.index = index
        self.timestamp = str(timestamp)
    
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        
        
    def calculate_hash(self):
        block_string = json.dumps(
            {
                
                
                
                
            })
        
