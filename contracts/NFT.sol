// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "./WhiteList.sol";

contract NFT is ERC721URIStorage {
    // White-List contract address constant
    WhiteList private _WLContract;
    uint256[] public tokenIds;

    constructor(
        string memory _name,
        string memory _symbol,
        WhiteList _whiteList
    ) ERC721(_name, _symbol) {
        _WLContract = _whiteList;
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override {
        require(
            _isWhiteListed(to),
            "ERC721: destination address is not white-listed"
        );
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function safeMint(address _to, uint256 _tokenId) public {
        tokenIds.push(_tokenId);
        _safeMint(_to, _tokenId);
    }

    function setTokenURI(uint256 _tokenId, string memory _uri) public {
        _setTokenURI(_tokenId, _uri);
    }

    function getTokenIds() public view returns (uint256[] memory) {
        return tokenIds;
    }

    /**
     * @dev Validates the 'to' if white listed
     */
    function _isWhiteListed(address _user) private returns (bool) {
        return _WLContract.isWhiteList(address(this), _user);
    }
}
