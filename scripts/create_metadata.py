import json
from brownie import AdvancedCollectable, network
from scripts.helpful_scripts import get_breed
from scripts.upload_to_pinata import upload_pinata
from scripts.sample_metadata import metadata_template
from pathlib import Path
import requests
import ipfshttpclient


def main():
    advanced_collectable = AdvancedCollectable[-1]
    number_0f_advance_collectables = advanced_collectable.tokenCounter()
    print(f"You have cerated {number_0f_advance_collectables} collectables....")
    for token_id in range(number_0f_advance_collectables):
        breed = get_breed(advanced_collectable.tokenIdToBreed(token_id))
        metadate_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectable_metadata = metadata_template
        if Path(metadate_file_name).exists():
            print(f"{metadate_file_name} is already exist, deleted to overwrite")
        else:
            print(f"Creating metadata file: {metadate_file_name}")
            collectable_metadata["name"] = breed
            collectable_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_ipfs_pinata(image_path)
            collectable_metadata["image"] = image_uri
            with open(metadate_file_name, "w") as file:
                json.dump(collectable_metadata, file)
            print(f"uploaded to IPFS as : {upload_ipfs_pinata(metadate_file_name)}")


def upload_ipfs_pinata(file_path):
    hash = upload_pinata(file_path)
    return create_ipfs_uri(hash, file_path)


def create_ipfs_uri(hash, file_path):
    filename = file_path.split("/")[-1:][0]
    image_uri = f"https://ipfs.io/ipfs/{hash}?filename={filename}"
    # print(image_uri)
    return image_uri


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        api = ipfshttpclient.connect()
        res = api.add(file_path)
        # print(res)
        ipfs_hash = res["Hash"]
        filename = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        # print(image_uri)
        return image_uri
