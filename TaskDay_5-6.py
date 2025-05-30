


#Implement dynamic difficulty adjustment
#Add nonce to your Block class
#Implement mine_block(difficulty) method
#Test mining with difficulties 1, 2, and 4
#Measure and compare mining times
#Add difficulty property to Blockchain class
#Modify add_block() to mine blocks automatically
#Implement mining rewards
#Create a simple "miner" that can mine pending transactions

import hashlib
import json
import time
from datetime import datetime
from Day1_Blockchain import Block

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
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

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Set mining difficulty
    
    def create_genesis_block(self):
        return Block(0, datetime.now(), {"message": "Genesis Block"}, "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    # ✅ Modify add_block to mine before adding:
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)  # Mine the block!
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True


# Test the mining functionality
if __name__ == "__main__":
    print("🚀 Testing Proof of Work Mining!")
    
    # Create blockchain
    my_blockchain = Blockchain()
    
    # Test different difficulties
    print("\n1️⃣ Testing Difficulty 1:")
    my_blockchain.difficulty = 1
    start_time = time.time()
    my_blockchain.add_block(Block(1, datetime.now(), {"amount": 100, "sender": "Alice", "receiver": "Bob"}, ""))
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds\n")
    
    print("2️⃣ Testing Difficulty 2:")
    my_blockchain.difficulty = 2
    start_time = time.time()
    my_blockchain.add_block(Block(2, datetime.now(), {"amount": 200, "sender": "Bob", "receiver": "Charlie"}, ""))
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds\n")
    
    print("3️⃣ Testing Difficulty 4:")
    my_blockchain.difficulty = 4
    start_time = time.time()
    my_blockchain.add_block(Block(3, datetime.now(), {"amount": 300, "sender": "Charlie", "receiver": "Dave"}, ""))
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds\n")
    
    # Display results
    print("🔗 Final Blockchain:")
    for block in my_blockchain.chain:
        print(f"Block {block.index}: {block.hash[:16]}... (nonce: {block.nonce})")
    
    print(f"\n✅ Blockchain valid: {my_blockchain.is_chain_valid()}")