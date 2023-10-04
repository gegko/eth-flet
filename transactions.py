import os
import requests
from dotenv import load_dotenv
from web3 import Web3


load_dotenv()
api_key = os.getenv('ETHSCAN')

base_url = 'https://api.etherscan.io/api?module=account'
params = {
        "action": "txlist",
        "address": 0,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 10,
        "sort": "desc",
        "apikey": api_key,
    }


def get_last_5(eth_address: str) -> str:
    params['address'] = eth_address
    transactions_str = ''
    r = requests.get(base_url, params=params)
    result = r.json()['result']

    if result:    
        for i in result:
            value = int(i['value'])
            if i['from'] == eth_address:
                transactions_str += (
                    f"{Web3.from_wei(value, 'ether'):.10f} ETH | to: {i['to']} \n"
                )
            else:
                transactions_str += (
                    f"{Web3.from_wei(value, 'ether'):.10f} ETH | from: {i['from']} \n"
                )
    else:
        transactions_str = 'No transactions detected.'
    
    return transactions_str
