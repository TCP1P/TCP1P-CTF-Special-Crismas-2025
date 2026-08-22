// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

interface IElfHub {
    function getSharePrice() external view returns (uint256);
}

contract SantaLending {
    IElfHub public hub;
    mapping(address => uint256) public collateral;
    uint256 constant LIQUIDATION_THRESHOLD = 1 ether;

    constructor(address _hub) {
        hub = IElfHub(_hub);
    }

    function addCollateral(uint256 amount) external {
        collateral[msg.sender] += amount;
    }

    function isSolvent(address user) public view returns (bool) {
        if (collateral[user] == 0) return false;

        uint256 price = hub.getSharePrice();
        uint256 totalValue = (collateral[user] * price) / 1e18;

        return totalValue >= 50 ether;
    }

    function liquidate(address user) external {
        require(!isSolvent(user), "User is solvent!");

        uint256 amount = collateral[user];
        collateral[user] = 0;
        collateral[msg.sender] += amount;
    }

    function cheat_setCollateral(address user, uint256 amount) external {
        collateral[user] = amount;
    }
}
