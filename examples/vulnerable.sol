// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

contract Vault {
    mapping(address => uint256) public balances;
    address public owner;

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        (bool ok, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] = 0;
    }

    function setOwner(address next) external {
        owner = next;
    }

    function random() external view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty))) % 100;
    }

    function isExpired() external view returns (bool) {
        return block.timestamp > 1700000000;
    }

    function withdrawAll() external {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
