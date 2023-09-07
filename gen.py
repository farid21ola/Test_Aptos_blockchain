import asyncio
import json

from aptos_sdk.account import Account

AptURL = "https://fullnode.mainnet.aptoslabs.com/v1"
AptURLdn = "https://fullnode.devnet.aptoslabs.com/v1"
faucetURL = "https://faucet.devnet.aptoslabs.com"

wal = {'wallet': []}


async def gen(n: int):
    for i in range(n):
        wallet = Account.generate()
        pvk = wallet.private_key
        puk = wallet.public_key()
        wal['wallet'].append({
            'address': str(wallet.address()),
            'public_key': str(puk),
            'private_key': str(pvk),
        })

    print(wal)
    with open('wallets/data.txt', 'w') as outfile:
        json.dump(wal, outfile)

# Количество сгенерированных аккаунтов
n = 100
asyncio.run(gen(n))
