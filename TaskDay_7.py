import time
import hashlib
import json
from datetime import datetime
import random
import string

# Day 7 Tasks: Step-by-Step Implementation
# This file contains the specific daily tasks for Day 7A and Day 7B

print("📚 Day 7 Tasks: Building Transaction System Step by Step")
print("="*60)

#=============================================================================
# DAY 7A TASKS: Transaction System Foundation
#=============================================================================

print("\n🎯 DAY 7A TASKS: Transaction System Foundation")
print("-" * 50)

#-----------------------------------------------------------------------------
# Task 7A-1: Create a Transaction Class
#-----------------------------------------------------------------------------
print("\n✅ Task 7A-1: Create a Transaction Class")

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()
        self.transaction_id = self.generate_transaction_id()
        self.hash = self.calculate_hash()
    
    def generate_transaction_id(self):
        """Generate a unique transaction ID"""
        unique_string = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}{random.randint(1000, 9999)}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:12]
    
    def calculate_hash(self):
        """Calculate transaction hash for integrity"""
        transaction_string = json.dumps({
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": str(self.timestamp),
            "transaction_id": self.transaction_id
        }, sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def to_dict(self):
        """Convert transaction to dictionary for JSON serialization"""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": str(self.timestamp),
            "hash": self.hash
        }
    
    def __repr__(self):
        return f"TX({self.sender} → {self.receiver}: {self.amount})"

# Test Task 7A-1
print("   Testing Transaction Class:")
tx1 = Transaction("Alice", "Bob", 50)
tx2 = Transaction("Bob", "Charlie", 30)

print(f"   Transaction 1: {tx1}")
print(f"   TX ID: {tx1.transaction_id}")
print(f"   Hash: {tx1.hash[:16]}...")
print(f"   Transaction 2: {tx2}")
print(f"   ✅ Task 7A-1 Complete: Transaction class working!")

#-----------------------------------------------------------------------------
# Task 7A-2: Modify Block Class for Transactions
#-----------------------------------------------------------------------------
print("\n✅ Task 7A-2: Modify Block Class for Transactions")

class TransactionBlock:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions  # Changed from 'data' to 'transactions'
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate block hash including all transaction data"""
        # Convert transactions to dictionaries for hashing
        transactions_data = [tx.to_dict() for tx in self.transactions]
        
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": transactions_data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def display_transactions(self):
        """Display all transactions in the block"""
        print(f"   Block #{self.index} contains {len(self.transactions)} transactions:")
        for i, tx in enumerate(self.transactions, 1):
            print(f"      {i}. {tx.sender} sent {tx.amount} to {tx.receiver}")
    
    def __repr__(self):
        return f"Block({self.index}, {len(self.transactions)} txs)"

# Test Task 7A-2
print("   Testing Block with Transactions:")
transactions = [tx1, tx2]
block = TransactionBlock(1, datetime.now(), transactions, "previous_hash_123")

print(f"   Block created: {block}")
print(f"   Block hash: {block.hash[:16]}...")
block.display_transactions()
print(f"   ✅ Task 7A-2 Complete: Block now handles transactions!")

#-----------------------------------------------------------------------------
# Task 7A-3: Create Pending Transactions Pool
#-----------------------------------------------------------------------------
print("\n✅ Task 7A-3: Create Pending Transactions Pool")

class BasicBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []  # Transaction pool
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        return TransactionBlock(0, datetime.now(), [], "0")
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def create_transaction(self, transaction):
        """Add transaction to pending pool"""
        self.pending_transactions.append(transaction)
        print(f"   📝 Added to pool: {transaction}")
    
    def mine_pending_transactions(self):
        """Mine all pending transactions into a block"""
        if not self.pending_transactions:
            print("   ⚠️  No pending transactions to mine!")
            return
        
        print(f"   ⛏️  Mining {len(self.pending_transactions)} pending transactions...")
        
        new_block = TransactionBlock(
            index=len(self.chain),
            timestamp=datetime.now(),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )
        
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear pending transactions
        
        print(f"   ✅ Block #{new_block.index} mined and added to blockchain!")
        return new_block

# Test Task 7A-3
print("   Testing Pending Transactions Pool:")
blockchain = BasicBlockchain()

print(f"   Initial pending transactions: {len(blockchain.pending_transactions)}")

# Add transactions to pool
blockchain.create_transaction(Transaction("Alice", "Bob", 25))
blockchain.create_transaction(Transaction("Bob", "Charlie", 15))

print(f"   Pending transactions after adding: {len(blockchain.pending_transactions)}")

# Mine the pending transactions
mined_block = blockchain.mine_pending_transactions()
print(f"   Pending transactions after mining: {len(blockchain.pending_transactions)}")
print(f"   Blockchain now has {len(blockchain.chain)} blocks")
print(f"   ✅ Task 7A-3 Complete: Transaction pool system working!")

print(f"\n🎉 DAY 7A TASKS COMPLETED!")
print(f"✅ Transaction Class with IDs and hashes")
print(f"✅ Blocks that handle multiple transactions") 
print(f"✅ Pending transaction pool system")

#=============================================================================
# DAY 7B TASKS: Wallet System and Mining Economy
#=============================================================================

print(f"\n\n🎯 DAY 7B TASKS: Wallet System and Mining Economy")
print("-" * 50)

#-----------------------------------------------------------------------------
# Task 7B-1: Build a Basic Wallet Class
#-----------------------------------------------------------------------------
print("\n✅ Task 7B-1: Build a Basic Wallet Class")

class BasicWallet:
    def __init__(self, name=None):
        self.name = name or f"User_{random.randint(1000, 9999)}"
        self.address = self.generate_address()
        print(f"   💳 Created wallet '{self.name}' with address: {self.address}")
    
    def generate_address(self):
        """Generate a unique wallet address (simplified)"""
        # Create a simple address using random characters
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        return f"1{random_part}"  # Bitcoin-like format starting with '1'
    
    def send_money(self, receiver_address, amount):
        """Create a transaction from this wallet"""
        transaction = Transaction(self.address, receiver_address, amount)
        print(f"   📤 {self.name} created transaction: {transaction}")
        return transaction
    
    def __repr__(self):
        return f"Wallet({self.name}, {self.address[:12]}...)"

# Test Task 7B-1
print("   Testing Basic Wallet Class:")
alice_wallet = BasicWallet("Alice")
bob_wallet = BasicWallet("Bob")
charlie_wallet = BasicWallet("Charlie")

print(f"   Alice's address: {alice_wallet.address}")
print(f"   Bob's address: {bob_wallet.address}")

# Test transaction creation
tx = alice_wallet.send_money(bob_wallet.address, 100)
print(f"   Transaction created: {tx}")
print(f"   ✅ Task 7B-1 Complete: Basic wallet system working!")

#-----------------------------------------------------------------------------
# Task 7B-2: Implement Balance Calculation
#-----------------------------------------------------------------------------
print("\n✅ Task 7B-2: Implement Balance Calculation")

class WalletWithBalance(BasicWallet):
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
                        print(f"   💰 {self.name} received {tx.amount} (balance: {balance})")
                    
                    # Subtract sent amounts
                    if tx.sender == self.address:
                        balance -= tx.amount
                        print(f"   💸 {self.name} sent {tx.amount} (balance: {balance})")
        
        return balance

# Test Task 7B-2
print("   Testing Balance Calculation:")

# Create wallets with balance capability
alice = WalletWithBalance("Alice")
bob = WalletWithBalance("Bob")

# Create blockchain with some transactions
blockchain = BasicBlockchain()

# Add transactions involving Alice and Bob
blockchain.create_transaction(Transaction("System", alice.address, 100))  # Alice receives 100
blockchain.create_transaction(Transaction(alice.address, bob.address, 30))  # Alice sends 30 to Bob

# Mine the transactions
blockchain.mine_pending_transactions()

# Check balances
print(f"   Calculating balances after transactions:")
alice_balance = alice.get_balance(blockchain)
bob_balance = bob.get_balance(blockchain)

print(f"   Alice's balance: {alice_balance}")
print(f"   Bob's balance: {bob_balance}")
print(f"   ✅ Task 7B-2 Complete: Balance calculation working!")

#-----------------------------------------------------------------------------
# Task 7B-3: Add Mining Rewards
#-----------------------------------------------------------------------------
print("\n✅ Task 7B-3: Add Mining Rewards")

class BlockchainWithMining(BasicBlockchain):
    def __init__(self):
        super().__init__()
        self.mining_reward = 10  # Reward for mining a block
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mine pending transactions and reward the miner"""
        if not self.pending_transactions:
            print("   ⚠️  No pending transactions to mine!")
            return
        
        print(f"   ⛏️  Mining {len(self.pending_transactions)} transactions...")
        
        # Create mining reward transaction
        mining_reward_tx = Transaction("System", mining_reward_address, self.mining_reward)
        print(f"   💎 Mining reward: {mining_reward_tx}")
        
        # Add mining reward to the transactions
        all_transactions = [mining_reward_tx] + self.pending_transactions
        
        new_block = TransactionBlock(
            index=len(self.chain),
            timestamp=datetime.now(),
            transactions=all_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        print(f"   ✅ Block #{new_block.index} mined! Miner earned {self.mining_reward} coins")
        return new_block

# Test Task 7B-3
print("   Testing Mining Rewards:")

# Create blockchain with mining rewards
blockchain_with_mining = BlockchainWithMining()

# Create miner wallet
miner = WalletWithBalance("Miner")
alice = WalletWithBalance("Alice")
bob = WalletWithBalance("Bob")

print(f"   Initial balances:")
print(f"   Miner: {miner.get_balance(blockchain_with_mining)}")
print(f"   Alice: {alice.get_balance(blockchain_with_mining)}")

# Add some transactions to mine
blockchain_with_mining.create_transaction(Transaction(alice.address, bob.address, 5))

# Mine transactions (miner gets reward)
print(f"   Mining transactions with miner as reward recipient:")
blockchain_with_mining.mine_pending_transactions(miner.address)

# Check balances after mining
print(f"   Balances after mining:")
print(f"   Miner: {miner.get_balance(blockchain_with_mining)} (should have earned {blockchain_with_mining.mining_reward})")
print(f"   ✅ Task 7B-3 Complete: Mining rewards working!")

print(f"\n🎉 DAY 7B TASKS COMPLETED!")
print(f"✅ Basic wallet class with unique addresses")
print(f"✅ Balance calculation by blockchain scanning")
print(f"✅ Mining rewards system")

#=============================================================================
# FINAL DEMONSTRATION: All Day 7 Tasks Working Together
#=============================================================================

print(f"\n\n🚀 FINAL DEMO: All Day 7 Tasks Working Together")
print("="*60)

def demonstrate_all_day7_tasks():
    """Demonstrate all Day 7 tasks working together"""
    
    # Create blockchain with mining
    blockchain = BlockchainWithMining()
    
    # Create wallets
    alice = WalletWithBalance("Alice")
    bob = WalletWithBalance("Bob")
    charlie = WalletWithBalance("Charlie")
    miner = WalletWithBalance("Miner")
    
    print(f"\n📊 Initial State:")
    print(f"   Blockchain has {len(blockchain.chain)} blocks")
    print(f"   Pending transactions: {len(blockchain.pending_transactions)}")
    
    # Step 1: Mine initial block to give miner some coins
    print(f"\n🎯 Step 1: Initial mining (create coins)")
    blockchain.mine_pending_transactions(miner.address)
    
    print(f"   Miner balance: {miner.get_balance(blockchain)}")
    
    # Step 2: Miner sends coins to Alice and Bob
    print(f"\n🎯 Step 2: Miner distributes coins")
    tx1 = miner.send_money(alice.address, 4)
    tx2 = miner.send_money(bob.address, 3)
    
    blockchain.create_transaction(tx1)
    blockchain.create_transaction(tx2)
    
    # Mine these transactions
    blockchain.mine_pending_transactions(miner.address)
    
    print(f"   Balances after distribution:")
    print(f"   Miner: {miner.get_balance(blockchain)}")
    print(f"   Alice: {alice.get_balance(blockchain)}")
    print(f"   Bob: {bob.get_balance(blockchain)}")
    
    # Step 3: Alice and Bob send to Charlie
    print(f"\n🎯 Step 3: Multiple transactions")
    tx3 = alice.send_money(charlie.address, 2)
    tx4 = bob.send_money(charlie.address, 1)
    
    blockchain.create_transaction(tx3)
    blockchain.create_transaction(tx4)
    
    # Mine final block
    blockchain.mine_pending_transactions(miner.address)
    
    print(f"   Final balances:")
    print(f"   Miner: {miner.get_balance(blockchain)}")
    print(f"   Alice: {alice.get_balance(blockchain)}")
    print(f"   Bob: {bob.get_balance(blockchain)}")
    print(f"   Charlie: {charlie.get_balance(blockchain)}")
    
    print(f"\n📊 Final Statistics:")
    print(f"   Total blocks: {len(blockchain.chain)}")
    total_txs = sum(len(block.transactions) for block in blockchain.chain if hasattr(block, 'transactions'))
    print(f"   Total transactions: {total_txs}")
    
    return blockchain

# Run the complete demonstration
final_blockchain = demonstrate_all_day7_tasks()

print(f"\n🏆 CONGRATULATIONS!")
print(f"✅ All Day 7 Tasks completed successfully!")
print(f"✅ You have built a working transaction system with:")
print(f"   • Transaction class with unique IDs")
print(f"   • Blocks that handle multiple transactions")
print(f"   • Pending transaction pool")
print(f"   • Digital wallets with unique addresses")
print(f"   • Balance calculation system")
print(f"   • Mining rewards economy")
print(f"\n🎉 Your cryptocurrency foundation is complete!")