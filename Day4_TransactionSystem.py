import time
import hashlib
import json
from datetime import datetime


###
#1. Create a Transaction Class 🏦
#Build a proper transaction system that tracks:

#Sender and Receiver addresses
#Amount being transferred
#Transaction signatures (digital signatures for security)
#Transaction fees
#Timestamp and unique transaction ID

#2. Build a Wallet System 👛
#Create digital wallets that can:

#Generate unique addresses (like Bitcoin addresses)
#Store private/public key pairs
#Sign transactions to prove ownership
#Check balance across the entire blockchain
#Create and send transactions

#3. Implement UTXO or Account Model 💰
#Choose one approach:

#UTXO Model (like Bitcoin): Track unspent transaction outputs
#Account Model (like Ethereum): Keep running balance for each address

#4. Add Transaction Validation ✅
#Ensure transactions are valid:

#Sufficient balance check
#Valid signatures verification
#No double-spending prevention
#Transaction fee calculation

#5. Mining Rewards & Transaction Fees 💎
#Implement the economic incentives:

#Block rewards for miners
#Transaction fees paid to miners
#Coinbase transactions (mining rewards)


#Real-World Features You'll Build:
#🎯 Day 7 Deliverables:

#Transaction System: Send money between wallets
#Digital Signatures: Cryptographically secure transactions
#Balance Tracking: Calculate wallet balances
#Mining Economy: Miners earn rewards + fees
#Transaction Pool: Pending transactions waiting to be mined
#Wallet Management: Generate addresses, sign transactions

#🧪 Testing Scenarios:

#Create 3 wallets (Alice, Bob, Charlie)
#Give Alice initial coins through mining
#Alice sends coins to Bob
#Bob sends coins to Charlie
#Verify all balances are correct
#Try invalid transactions (insufficient funds, bad signatures)


###




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


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100

    
    
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
    
    def mine_pending_transactions(self,mining_reward_address):
        
        pass


class Transaction:
 def __init__(self,sender,receiver,amount,fee):
    self.sender=sender
    self.receiver=receiver
    self.amount=amount
    self.fee=fee
    
class Wallet:
    def __init__(self):
        # Generate public/private key pair
        # Create unique address
        pass
    
    def get_balance(self,blockchain):
        #Calculate Balance from entire blockchain
        
        pass
    
    def send_money(self,receiver_address,amount,blockchain):
        #Create and sign transaction
        
        pass
    
    
    
