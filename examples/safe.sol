// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

contract SafeVault {
    mapping(address => uint256) public balances;
    address public immutable owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor(address owner_) {
        owner = owner_;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }

    function setFee(uint256 fee) external onlyOwner {
        require(fee <= 100, "fee too high");
        balances[owner] = fee;
    }
}
