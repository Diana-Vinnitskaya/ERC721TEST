// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyERC721 is ERC721, ERC721Enumerable, Ownable {

    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    uint256 public constant max_supply = 100;
    uint256 public constant mint_limit = 3;
    uint256 public constant price_per_token = 0.001 ether;
    uint256 public constant limit_for_address = 6;

    address private withdrawalReceiver;

    constructor(address _withdrawalReceiver) ERC721("My NFT", "MNFT") {
        withdrawalReceiver = _withdrawalReceiver;
    }

    function getWithdrawalReceiver() public view returns (address)
    {
        return withdrawalReceiver;
    }

    function _balance() public view returns (uint256)
    {
        return payable(address(this)).balance;
    }
    
    function _beforeTokenTransfer(address from, address to, uint256 tokenId)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId);
    }
    
    function mint(uint256 numberOfTokens) external payable {
        require(totalSupply() + numberOfTokens <= max_supply, "Exceeds max supply");
        require(numberOfTokens <= mint_limit, "Exceeds mint limit");
        require(totalTokensOf(msg.sender) + numberOfTokens <= limit_for_address, "Exceeds token limit for the address");
        require(msg.value == numberOfTokens * price_per_token, "Incorrect ether amount");

        for (uint256 i = 0; i < numberOfTokens; i++) {
            uint256 tokenId = _tokenIdCounter.current();
            _safeMint(msg.sender, tokenId);
            _tokenIdCounter.increment();
        }
    }

    function withdraw() external onlyOwner {
        payable(withdrawalReceiver).transfer(_balance());
    }

    function totalTokensOf(address _owner) public view returns (uint256) {
        return balanceOf(_owner);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function contractURI() public pure returns (string memory) {
        return "https://bafybeibc5sgo2plmjkq2tzmhrn54bk3crhnc23zd2msg4ea7a4pxrkgfna.ipfs.dweb.link/";
    }
}

