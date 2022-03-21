from brownie import NFTManager, config, network, NFT, convert
from web3 import Web3 as w3
from scripts.helpful_scripts import get_account, OPENSEA_URL


def main():
    # show_manager_address()
    deploy_manager()
    # add_white_list("0x836af64dE9621c53a0Fb59Cd5d04Fc75F6982Fac")
    # mint_nft(
    #     "https://gateway.pinata.cloud/ipfs/QmW4qPbedTL7DS3AgdzMnrw7YKYZB2miLAywJBNZe97kTz",
    # )
    # create_collection("Snap Innovations 2", "SI2")


def show_manager_address():
    manager = NFTManager[-1]
    print(f"Last manager deployed: {manager.address}")


def deploy_manager():
    account = get_account()
    manager = NFTManager.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"NFT manager has been deployed at {manager}")


def add_white_list(_user):
    account = get_account()
    manager = NFTManager[-1]
    collection_addresses = manager.getCollections(account.address)
    _collection = NFT.at(collection_addresses[-1])
    tx = manager.addWhiteList(_collection, _user, {"from": account})
    tx.wait(1)
    print(f"Address {_user} added as a whitelist user for collection {_collection}")


def mint_nft(_uri):
    account = get_account()
    manager = NFTManager[-1]
    collection_addresses = manager.getCollections(account.address)
    print(f"collections addresses {collection_addresses[- 1]}")
    token_id = len(collection_addresses)
    print(f"token ID is: {token_id}")
    collection = NFT.at(collection_addresses[-1])
    tx_minting = collection.safeMint(account.address, token_id, {"from": account})
    tx_minting.wait(1)
    tx_uri = collection.setTokenURI(token_id, _uri, {"from": account})
    tx_uri.wait(1)
    print(
        f"token is updated, you can check it out in the link below\n *Note: please wait 20minutes for info to be propogate\n{OPENSEA_URL.format(collection.address, token_id)}"
    )


def create_collection(_name, _symbol):
    account = get_account()
    manager = NFTManager[-1]
    tx_creating_collection = manager.createCollection(_name, _symbol, {"from": account})
    tx_creating_collection.wait(1)
    print(f"collection created at {manager.owners_collections(account.address,0)}")
