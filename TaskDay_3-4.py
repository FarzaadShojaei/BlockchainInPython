# Day3_4_ExtendedBlockchain.py
# This file imports your existing Block and Blockchain classes and extends them

import json
from datetime import datetime
from Day1_Blockchain import Block  # Import your Block class
from Day2_CreatingBlockchain import Blockchain  # Import your Blockchain class

class ExtendedBlockchain(Blockchain):
    """
    Extended Blockchain class that inherits from your original Blockchain
    and adds the Day 3-4 functionality:
    1. Display entire blockchain nicely
    2. Find block by index
    3. Simple CLI interface
    """
    
    def __init__(self):
        # Call parent constructor to initialize the basic blockchain
        super().__init__()
    
    # ✅ Task 1: Display the entire blockchain nicely
    def display_blockchain(self):
        """Display the entire blockchain in a nice, readable format"""
        print("=" * 60)
        print("               BLOCKCHAIN DISPLAY")
        print("=" * 60)
        
        for i, block in enumerate(self.chain):
            print(f"\n📦 BLOCK #{block.index}")
            print(f"   Hash: {block.hash}")
            print(f"   Previous Hash: {block.previous_hash}")
            print(f"   Timestamp: {block.timestamp}")
            print(f"   Data: {json.dumps(block.data, indent=8)}")
            
            # Add visual connection between blocks
            if i < len(self.chain) - 1:
                print("   ⬇️  links to")
        
        print(f"\n✅ Chain Status: {'VALID' if self.is_chain_valid() else 'INVALID'}")
        print(f"📊 Total blocks: {len(self.chain)}")
    
    # ✅ Task 2: Find a block by its index
    def find_block_by_index(self, index):
        """Find and return a block by its index"""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        else:
            return None
    
    def display_block_info(self, index):
        """Display detailed information for a specific block"""
        block = self.find_block_by_index(index)
        
        if block:
            print(f"\n🔍 BLOCK #{index} DETAILS")
            print(f"   Hash: {block.hash}")
            print(f"   Previous Hash: {block.previous_hash}")
            print(f"   Timestamp: {block.timestamp}")
            print(f"   Data: {json.dumps(block.data, indent=8)}")
            if hasattr(block, 'nonce'):
                print(f"   Nonce: {block.nonce}")
        else:
            print(f"❌ Block with index {index} not found!")
            print(f"   Available indices: 0 to {len(self.chain)-1}")
    
    def get_blockchain_stats(self):
        """Get comprehensive statistics about the blockchain"""
        return {
            "total_blocks": len(self.chain),
            "is_valid": self.is_chain_valid(),
            "latest_block_hash": self.get_latest_block().hash,
            "genesis_block_hash": self.chain[0].hash,
            "latest_block_index": self.get_latest_block().index
        }
    
    # ✅ Task 3: Simple CLI to interact with blockchain
    def simple_cli(self):
        """Simple command line interface for blockchain interaction"""
        print("\n🔗 Welcome to Extended Blockchain CLI!")
        print("This CLI uses your imported Block and Blockchain classes.")
        
        while True:
            self._display_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self._cli_display_blockchain()
            elif choice == '2':
                self._cli_find_block()
            elif choice == '3':
                self._cli_add_block()
            elif choice == '4':
                self._cli_validate_chain()
            elif choice == '5':
                self._cli_show_stats()
            elif choice == '6':
                self._cli_tamper_block()
            elif choice == '7':
                print("\n👋 Thank you for using Extended Blockchain CLI! Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please select 1-7.")
            
            input("\nPress Enter to continue...")
    
    def _display_menu(self):
        """Display the CLI menu"""
        print("\n" + "="*50)
        print("🔗 EXTENDED BLOCKCHAIN CLI MENU")
        print("="*50)
        print("1. 📋 Display entire blockchain")
        print("2. 🔍 Find block by index")
        print("3. ➕ Add new block")
        print("4. ✅ Validate blockchain")
        print("5. 📊 Show blockchain statistics")
        print("6. 🔨 Tamper with block (for testing)")
        print("7. 🚪 Exit")
        print("="*50)
    
    def _cli_display_blockchain(self):
        """CLI method to display blockchain"""
        self.display_blockchain()
    
    def _cli_find_block(self):
        """CLI method to find and display a block"""
        try:
            index = int(input("Enter block index to find: "))
            self.display_block_info(index)
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def _cli_add_block(self):
        """CLI method to add a new block"""
        print("\n➕ Adding new block...")
        
        # Get transaction data from user
        sender = input("Enter sender: ")
        receiver = input("Enter receiver: ")
        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("⚠️  Invalid amount, setting to 0")
            amount = 0
        
        # Create block data
        block_data = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": str(datetime.now())
        }
        
        # Create new block using your imported Block class
        new_index = len(self.chain)
        new_block = Block(new_index, datetime.now(), block_data, "")
        
        # Add block using inherited method
        self.add_block(new_block)
        
        print(f"✅ Block #{new_index} added successfully!")
        print(f"   Hash: {new_block.hash[:16]}...")
    
    def _cli_validate_chain(self):
        """CLI method to validate the blockchain"""
        is_valid = self.is_chain_valid()
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"\n🔍 Blockchain validation: {status}")
        
        if not is_valid:
            print("   The blockchain has been tampered with or corrupted!")
    
    def _cli_show_stats(self):
        """CLI method to show blockchain statistics"""
        stats = self.get_blockchain_stats()
        print("\n📊 BLOCKCHAIN STATISTICS")
        print(f"   Total blocks: {stats['total_blocks']}")
        print(f"   Is valid: {'✅ Yes' if stats['is_valid'] else '❌ No'}")
        print(f"   Latest block index: {stats['latest_block_index']}")
        print(f"   Latest block hash: {stats['latest_block_hash'][:16]}...")
        print(f"   Genesis block hash: {stats['genesis_block_hash'][:16]}...")
    
    def _cli_tamper_block(self):
        """CLI method to tamper with a block for educational purposes"""
        print("\n🔨 Tampering with blockchain (Educational purposes only!)")
        print("This will break the blockchain integrity to demonstrate validation.")
        
        try:
            index = int(input("Enter block index to tamper with (0 to {}): ".format(len(self.chain)-1)))
            block = self.find_block_by_index(index)
            
            if block:
                print(f"\nCurrent block data: {block.data}")
                
                if 'amount' in str(block.data):
                    new_amount = input("Enter new amount value: ")
                    
                    # Tamper with the data
                    if isinstance(block.data, dict) and 'amount' in block.data:
                        original_amount = block.data['amount']
                        block.data['amount'] = new_amount
                        print(f"✅ Tampered! Changed amount from {original_amount} to {new_amount}")
                    else:
                        # Handle string data or other formats
                        block.data = {"tampered_amount": new_amount, "original": block.data}
                        print(f"✅ Block {index} data has been modified!")
                    
                    print("🔍 Try validating the chain now to see the security in action!")
                else:
                    print("⚠️  This block doesn't have obvious 'amount' data.")
                    confirm = input("Tamper anyway? (y/n): ")
                    if confirm.lower() == 'y':
                        block.data = {"tampered": True, "original": block.data}
                        print("✅ Block data has been modified!")
            else:
                print(f"❌ Block {index} not found!")
                
        except ValueError:
            print("❌ Please enter a valid number!")

# Demo and testing functions
def create_sample_blockchain():
    """Create a sample blockchain with test data"""
    blockchain = ExtendedBlockchain()
    
    # Add some sample blocks using your imported Block class
    sample_transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50},
        {"sender": "Bob", "receiver": "Charlie", "amount": 30},
        {"sender": "Charlie", "receiver": "David", "amount": 20},
        {"sender": "David", "receiver": "Alice", "amount": 15}
    ]
    
    for i, transaction in enumerate(sample_transactions, 1):
        block = Block(i, datetime.now(), transaction, "")
        blockchain.add_block(block)
    
    return blockchain

def demo_functionality():
    """Demonstrate all the Day 3-4 functionality"""
    print("🚀 Day 3-4 Functionality Demo")
    print("Using your imported Block and Blockchain classes!")
    
    # Create sample blockchain
    blockchain = create_sample_blockchain()
    
    # Demo 1: Display blockchain
    print("\n1️⃣ DEMO: Display entire blockchain")
    blockchain.display_blockchain()
    
    # Demo 2: Find block by index
    print("\n2️⃣ DEMO: Find block by index")
    blockchain.display_block_info(2)
    blockchain.display_block_info(10)  # Will show error
    
    # Demo 3: Show stats
    print("\n3️⃣ DEMO: Blockchain statistics")
    stats = blockchain.get_blockchain_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Ask if user wants to try the CLI
    print("\n4️⃣ INTERACTIVE CLI")
    try_cli = input("Do you want to try the interactive CLI? (y/n): ")
    if try_cli.lower() == 'y':
        blockchain.simple_cli()
    else:
        print("Demo completed! You can run blockchain.simple_cli() anytime.")

if __name__ == "__main__":
    # Run the demo
    demo_functionality()