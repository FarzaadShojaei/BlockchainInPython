import time
import hashlib
import json
from datetime import datetime

##
#Task 7A-1: Create a Transaction Class
#Build a proper Transaction class that includes:

#Sender address, receiver address, amount
#Transaction timestamp and unique ID
#Method to calculate transaction hash
#Method to convert transaction to dictionary format for JSON serialization


#Task 7A-2: Modify Your Block Class
#Update your Block class to handle multiple transactions instead of simple data:

#Change data parameter to transactions (list of Transaction objects)
#Update calculate_hash() to include all transaction data
#Modify the display methods to show transaction details

#Task 7A-3: Create Pending Transactions Pool
#Modify your Blockchain class to:

#Add pending_transactions = [] property
#Create create_transaction(transaction) method to add transactions to the pool
#Modify mining to process pending transactions instead of single blocks



###