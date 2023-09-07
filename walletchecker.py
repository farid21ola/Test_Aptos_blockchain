import asyncio
import json

from aptos_sdk.account import Account
from aptos_sdk.async_client import FaucetClient, RestClient

from gen import AptURLdn, faucetURL

with open('wallets/data.txt') as file:
    wallets = json.load(file)


async def check():
    rest_client = RestClient(AptURLdn)
    faucet_client = FaucetClient(faucetURL, rest_client)

    accounts = []
    i = 0
    for w in wallets['wallet']:
        if i==3: break
        pvk = w['private_key']
        acc = Account.load_key(pvk)
        accounts.append(acc)
        i+=1
    print(len(accounts))
    # print("~~~~~~~~~~~~~~~Start Balance~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # ball_accs = []
    # for a in accounts:
    #     ball_accs.append(rest_client.account_balance(a.address()))
    # ball_accs = await asyncio.gather(*ball_accs)
    # for i in range(len(accounts)):
    #     print(accounts[i].address(), " Balance: ", ball_accs[i])

    fund_accs = []
    for a in accounts:
        fund_accs.append(faucet_client.fund_account(str(a.address()), 100_000_000))
    await asyncio.gather(*fund_accs)

    # txn_hash = await rest_client.transfer(accounts[0], accounts[1].address(), 1_000) #С главного акка на 100 других вот это и всё
    # await rest_client.wait_for_transaction(txn_hash) # это строчки переноса APT со своего кошелька на данный адрес

    print("\n~~~~~~~~~~~~~~~Final Balance~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    ball_accs = []
    for a in accounts:
        ball_accs.append(rest_client.account_balance(a.address()))
    ball_accs = await asyncio.gather(*ball_accs)
    for i in range(len(accounts)):
        print(accounts[i].address(), " Balance: ", ball_accs[i])

    await rest_client.close()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(check())
