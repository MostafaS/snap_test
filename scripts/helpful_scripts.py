from brownie import (
    accounts,
    network,
    config,
)

from web3 import Web3 as w3

# DEV_ENVIRONMENT = ["development", "mainnet-fork"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{} "


def get_account(index=None, id=None):
    # if index of an account has been passed - mostly the fake generated one by - ganach/brownie
    # here the account will be added one or fake created one by brownie/ganache
    if index:
        return accounts[index]

    # if an id has been passed, the added account will be returned
    if id:
        accounts.load(id)

    # if none of the index or id has been passed, we check which network it is and if its development/local
    # network, we will pass the zeroTH account of local development. could be forked or development
    if (
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS
        or network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]

    # and if the network is a live one, we get the private key from config/env and pass it
    return accounts.add(config["wallets"]["from_key"])
