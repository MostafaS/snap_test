// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "./NFT.sol";
import "./WhiteList.sol";

contract NFTManager {
    // collection => owner
    mapping(address => address) public collections_owners;
    // owner => array of collections
    mapping(address => address[]) public owners_collections;
    // collection => int32
    mapping(address => uint256[]) public tokenIds;
    // White-List contract address constant
    // ***for the purpose of testing this is not private***
    WhiteList public _WLContract;

    constructor() {
        _WLContract = new WhiteList();
    }

    /**  
        add an address to white list
     *****for the purpose of test, this function is public*****
        this function MUST be restricted through access control
        so no one other than approved addresses could call this 
    */
    function addWhiteList(address _collection, address _user)
        public
        returns (bool)
    {
        return _WLContract.addAddress(_collection, _user);
    }

    function createCollection(string memory _name, string memory _symbol)
        public
        returns (address)
    {
        NFT new_collection = new NFT(_name, _symbol, _WLContract);
        collections_owners[address(new_collection)] = msg.sender;
        owners_collections[msg.sender].push(address(new_collection));
        addWhiteList(address(new_collection), msg.sender);
        return address(new_collection);
    }

    // function createItem(address _collection) public returns (uint256) {
    //     NFT collection = NFT(_collection);
    //     uint256 tokenId = tokenIds[_collection].length;
    //     collection._safeMint(_collection, tokenId);
    //     tokenIds[_collection].push(tokenId);
    //     return (tokenId);
    // }

    function getCollections(address _owner)
        public
        view
        returns (address[] memory)
    {
        return owners_collections[_owner];
    }
}
