import asyncio
import json

from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient

import gen

with open('wallets/data.txt') as file:
    wallets = json.load(file)


async def transfer():
    rest_client = RestClient(gen.AptURL)

    accounts = []
    i = 0
    for w in wallets['wallet']:
        if i == 0:
            pvk = w['private_key']
            mainacc = Account.load_key(pvk)
        else:
            pvk = w['private_key']
            acc = Account.load_key(pvk)
            accounts.append(acc)
        i += 1

    for i in range(10):
        txn_hash = await rest_client.transfer(mainacc, accounts[i].address(), 1_000_000) #С главного акка на n перенос
        await rest_client.wait_for_transaction(txn_hash) # это две строчки переноса APT с одного кошелька на данный адрес

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(transfer())
