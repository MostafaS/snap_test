// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract WhiteList {
    // list of white-listed address(internal addresses) for each collection
    mapping(address => mapping(address => bool)) public white_list;

    // adding an address to the white-list
    function addAddress(address _collection, address _user)
        external
        returns (bool)
    {
        white_list[_collection][_user] = true;
        return (white_list[_collection][_user]);
    }

    // checking whether an address is white-listed or not
    function isWhiteList(address _collection, address _user)
        external
        view
        returns (bool)
    {
        return white_list[_collection][_user];
    }
}
