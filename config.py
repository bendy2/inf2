import logging
import os

from dotenv import load_dotenv
from eth_account import Account
from eth_utils import is_same_address
from web3 import Web3


logging.basicConfig(level=logging.INFO)

load_dotenv()

validation_errors = []


MASTER_PKEY = os.getenv("MASTER_PKEY")
MASTER_ADDRESS = os.getenv("MASTER_ADDRESS")
REWARDS_RECIPIENT_ADDRESS = os.getenv("REWARDS_RECIPIENT_ADDRESS")

if MASTER_PKEY is None:
    print(f"Error with MASTER_PKEY: set value in .env")
    exit(0)

try:
    master = Account.from_key(MASTER_PKEY)
except Exception:
    pk = MASTER_PKEY[:4] + "*" * (len(MASTER_PKEY) - 8) + MASTER_PKEY[-4:]
    print(f"Error with MASTER_PKEY: {pk} is not valid private key")
    exit(0)

if MASTER_ADDRESS is None:
    MASTER_ADDRESS = master.address
if REWARDS_RECIPIENT_ADDRESS is None:
    REWARDS_RECIPIENT_ADDRESS = master.address

if not is_same_address(MASTER_ADDRESS, master.address):
    print(f"Error with MASTER_ADDRESS: delete this value, its deprecated")
    exit(0)

if not is_same_address(master.address, REWARDS_RECIPIENT_ADDRESS):
    print(
        f"[WARNING]: make sure, that you have access to {REWARDS_RECIPIENT_ADDRESS} address"
    )

INFINITY_RPC = os.getenv("INFINITY_RPC")
INFINITY_WS = os.getenv("INFINITY_WS")
try:
    w3 = Web3(Web3.HTTPProvider(INFINITY_RPC))
    master_balance = w3.eth.get_balance(master.address)
except Exception:
    print(f"Error with INFINITY_RPC: can't establish connect with {INFINITY_RPC}")
    exit(0)

if master_balance < 10e18:
    print(
        f"[WARNING]: Current master balance is {master_balance/1e18:.2f} $S. Consider to top up it."
    )
