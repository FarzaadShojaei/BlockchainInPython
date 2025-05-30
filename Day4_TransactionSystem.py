import time
import hashlib
import json
from datetime import datetime
import random
import string

# Day 7 Challenge: Build a Complete Cryptocurrency System
# This file contains the 5 main challenges from Day 7

#=============================================================================
# Challenge 1: Create a Transaction Class 🏦
#=============================================================================
class Transaction:
    def __init__(self, sender, receiver, amount, fee=0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.timestamp = datetime.now()
        self.transaction_id = self.generate_transaction_id()
        self.signature = None
        self.hash = self.calculate_hash()
    
    def generate_transaction_id(self):
        """Generate unique transaction ID"""
        unique_string = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}{random.randint(1000, 9999)}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def calculate_hash(self):
        """Calculate transaction hash for integrity"""
        transaction_data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": str(self.timestamp),
            "transaction_id": self.transaction_id
        }
        transaction_string = json.dumps(transaction_data, sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def sign_transaction(self, private_key):
        """Digital signature for transaction security"""
        if self.sender == "System":  # Mining rewards don't need signatures
            self.signature = "SYSTEM_SIGNATURE"
        else:
            # Create signature from transaction hash + private key
            sign_data = f"{self.hash}{private_key}"
            self.signature = hashlib.sha256(sign_data.encode()).hexdigest()[:32]
    
    def is_valid(self):
        """Validate transaction structure and signature"""
        # Basic validation
        if not self.sender or not self.receiver or self.amount <= 0:
            return False
        
        # Signature validation (except for mining rewards)
        if self.sender != "System" and not self.signature:
            return False
        
        # Hash integrity check
        if self.hash != self.calculate_hash():
            return False
        
        return True
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": str(self.timestamp),
            "signature": self.signature,
            "hash": self.hash
        }
    
    def __repr__(self):
        return f"TX({self.sender[:8]}...→{self.receiver[:8]}...: {self.amount})"

#=============================================================================
# Challenge 2: Build a Wallet System 👛
#=============================================================================
class Wallet:
    def __init__(self, name=None):
        self.name = name or f"User_{random.randint(1000, 9999)}"
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()
        print(f"💳 Created wallet '{self.name}' with address: {self.address[:20]}...")
    
    def generate_private_key(self):
        """Generate unique private key"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    
    def generate_public_key(self):
        """Generate public key from private key"""
        return hashlib.sha256(self.private_key.encode()).hexdigest()
    
    def generate_address(self):
        """Generate Bitcoin-like wallet address"""
        # Create address from public key (simplified Bitcoin address format)
        address_data = f"1{self.public_key[:30]}"
        return address_data
    
    def get_balance(self, blockchain):
        """Calculate wallet balance by scanning entire blockchain"""
        balance = 0
        
        # Scan all blocks in the blockchain
        for block in blockchain.chain:
            # Skip genesis block (has no transactions)
            if hasattr(block, 'transactions') and block.transactions:
                for tx in block.transactions:
                    # Add received amounts
                    if tx.receiver == self.address:
                        balance += tx.amount
                    
                    # Subtract sent amounts and fees
                    if tx.sender == self.address:
                        balance -= (tx.amount + tx.fee)
        
        return balance
    
    def send_money(self, receiver_address, amount, fee=0):
        """Create and sign a transaction"""
        if not receiver_address or amount <= 0:
            raise ValueError("Invalid receiver address or amount")
        
        # Create transaction
        transaction = Transaction(self.address, receiver_address, amount, fee)
        
        # Sign transaction with private key
        transaction.sign_transaction(self.private_key)
        
        return transaction
    
    def __repr__(self):
        return f"Wallet({self.name}, {self.address[:16]}...)"

#=============================================================================
# Challenge 3: Enhanced Blockchain with Transaction Support
#=============================================================================
class EnhancedBlock:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions  # List of Transaction objects
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate block hash including all transaction data"""
        # Convert transactions to dictionaries
        transactions_data = [tx.to_dict() for tx in self.transactions]
        
        block_data = {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": transactions_data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine block with Proof of Work"""
        target = "0" * difficulty
        start_time = time.time()
        
        print(f"⛏️  Mining block #{self.index} with {len(self.transactions)} transactions...")
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            if self.nonce % 50000 == 0:
                print(f"   Trying nonce: {self.nonce}")
        
        end_time = time.time()
        print(f"✅ Block #{self.index} mined! Time: {end_time - start_time:.2f}s")
    
    def __repr__(self):
        return f"Block({self.index}, {len(self.transactions)} txs)"

#=============================================================================
# Challenge 4 & 5: Complete Blockchain with Mining Economy 💎
#=============================================================================
class CryptocurrencyBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3  # Mining difficulty
        self.pending_transactions = []  # Transaction pool
        self.mining_reward = 100  # Block reward for miners
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        return EnhancedBlock(0, datetime.now(), [], "0")
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def create_transaction(self, transaction):
        """Add transaction to pending pool after validation"""
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            print(f"📝 Transaction added: {transaction}")
        else:
            print(f"❌ Invalid transaction rejected: {transaction}")
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mine all pending transactions and reward the miner"""
        print(f"\n⛏️  Mining {len(self.pending_transactions)} pending transactions...")
        
        # Calculate total transaction fees
        total_fees = sum(tx.fee for tx in self.pending_transactions)
        
        # Create coinbase transaction (mining reward)
        mining_reward_tx = Transaction(
            sender="System",
            receiver=mining_reward_address,
            amount=self.mining_reward + total_fees,
            fee=0
        )
        mining_reward_tx.sign_transaction("SYSTEM_KEY")
        
        # Create block with all transactions
        all_transactions = [mining_reward_tx] + self.pending_transactions
        
        new_block = EnhancedBlock(
            index=len(self.chain),
            timestamp=datetime.now(),
            transactions=all_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to blockchain and clear pending transactions
        self.chain.append(new_block)
        self.pending_transactions = []
        
        print(f"💰 Miner earned: {self.mining_reward} (reward) + {total_fees} (fees) = {self.mining_reward + total_fees}")
        print(f"📦 Block #{new_block.index} added to blockchain!\n")
        
        return new_block
    
    def get_balance(self, address):
        """Get balance for any address"""
        balance = 0
        
        for block in self.chain:
            if hasattr(block, 'transactions'):
                for tx in block.transactions:
                    if tx.receiver == address:
                        balance += tx.amount
                    if tx.sender == address:
                        balance -= (tx.amount + tx.fee)
        
        return balance
    
    def is_chain_valid(self):
        """Validate entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Validate block hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Validate chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Validate all transactions
            for tx in current_block.transactions:
                if not tx.is_valid():
                    return False
        
        return True

#=============================================================================
# DEMONSTRATION: Complete Cryptocurrency in Action
#=============================================================================
def demonstrate_cryptocurrency():
    """Demonstrate all 5 Day 7 challenges working together"""
    print("🚀 Day 7 Challenge: Complete Cryptocurrency System")
    print("="*60)
    
    # Create blockchain
    blockchain = CryptocurrencyBlockchain()
    
    # Create wallets (Challenge 2)
    alice = Wallet("Alice")
    bob = Wallet("Bob")
    charlie = Wallet("Charlie")
    miner = Wallet("Miner")
    
    # Show initial balances
    print(f"\n💰 Initial Balances:")
    print(f"   Alice: {alice.get_balance(blockchain)} coins")
    print(f"   Bob: {bob.get_balance(blockchain)} coins")
    print(f"   Charlie: {charlie.get_balance(blockchain)} coins")
    print(f"   Miner: {miner.get_balance(blockchain)} coins")
    
    # Mine initial block to create coins (Challenge 5)
    print(f"\n🎯 Step 1: Initial mining to create cryptocurrency")
    blockchain.mine_pending_transactions(miner.address)
    print(f"   Miner now has: {miner.get_balance(blockchain)} coins")
    
    # Create transactions (Challenge 1)
    print(f"\n🎯 Step 2: Creating transactions")
    tx1 = miner.send_money(alice.address, 30, fee=1)
    tx2 = miner.send_money(bob.address, 25, fee=1)
    
    blockchain.create_transaction(tx1)
    blockchain.create_transaction(tx2)
    
    # Mine transaction block (Challenge 4 & 5)
    print(f"\n🎯 Step 3: Mining transaction block")
    blockchain.mine_pending_transactions(miner.address)
    
    # Show updated balances
    print(f"\n💰 Balances after transactions:")
    print(f"   Alice: {alice.get_balance(blockchain)} coins")
    print(f"   Bob: {bob.get_balance(blockchain)} coins")
    print(f"   Charlie: {charlie.get_balance(blockchain)} coins")
    print(f"   Miner: {miner.get_balance(blockchain)} coins")
    
    # More complex transactions
    print(f"\n🎯 Step 4: Complex transaction scenario")
    tx3 = alice.send_money(charlie.address, 10, fee=0.5)
    tx4 = bob.send_money(charlie.address, 15, fee=0.5)
    tx5 = charlie.send_money(alice.address, 5, fee=0.25)  # Charlie will get money first
    
    blockchain.create_transaction(tx3)
    blockchain.create_transaction(tx4)
    blockchain.create_transaction(tx5)
    
    # Mine final block
    blockchain.mine_pending_transactions(miner.address)
    
    # Final results
    print(f"\n💰 Final Balances:")
    print(f"   Alice: {alice.get_balance(blockchain)} coins")
    print(f"   Bob: {bob.get_balance(blockchain)} coins") 
    print(f"   Charlie: {charlie.get_balance(blockchain)} coins")
    print(f"   Miner: {miner.get_balance(blockchain)} coins")
    
    # Blockchain summary
    print(f"\n📊 Blockchain Summary:")
    print(f"   Total blocks: {len(blockchain.chain)}")
    print(f"   Blockchain valid: {blockchain.is_chain_valid()}")
    print(f"   Total transactions processed: {sum(len(block.transactions) for block in blockchain.chain if hasattr(block, 'transactions'))}")
    
    print(f"\n✅ All 5 Day 7 challenges completed successfully!")
    print(f"🎉 You've built a working cryptocurrency!")
    
    return blockchain, alice, bob, charlie, miner

if __name__ == "__main__":
    # Run the complete cryptocurrency demonstration
    blockchain, alice, bob, charlie, miner = demonstrate_cryptocurrency()
    
    # Show what you've accomplished
    print(f"\n🏆 CONGRATULATIONS! You've successfully implemented:")
    print(f"✅ Challenge 1: Complete Transaction System with signatures")
    print(f"✅ Challenge 2: Digital Wallet System with unique addresses") 
    print(f"✅ Challenge 3: Account Model for balance tracking")
    print(f"✅ Challenge 4: Transaction Validation and security")
    print(f"✅ Challenge 5: Mining Economy with rewards and fees")
    print(f"\n🚀 Your cryptocurrency is ready for the world!")