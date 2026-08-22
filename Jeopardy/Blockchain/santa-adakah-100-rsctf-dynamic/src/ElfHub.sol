// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "./ReentrancyGuard.sol";

contract ElfHub is ReentrancyGuard {
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    function deposit() external payable nonReentrant {
        uint256 shares = msg.value;
        if (totalSupply > 0 && address(this).balance > msg.value) {
            shares = (msg.value * totalSupply) / (address(this).balance - msg.value);
        }
        _mint(msg.sender, shares);
    }

    function withdraw(uint256 shares) external nonReentrant {
        require(balanceOf[msg.sender] >= shares, "Insufficient balance");

        uint256 amount = (shares * address(this).balance) / totalSupply;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        _burn(msg.sender, shares);
    }

    function getSharePrice() external view returns (uint256) {
        if (totalSupply == 0) return 1 ether;
        return (address(this).balance * 1e18) / totalSupply;
    }

    function _mint(address to, uint256 amount) internal {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function _burn(address from, uint256 amount) internal {
        balanceOf[from] -= amount;
        totalSupply -= amount;
    }
}
