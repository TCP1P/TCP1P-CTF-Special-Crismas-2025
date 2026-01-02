// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "./GiftDistributor.sol";

contract MockNiceList is INiceList {
    function isNice(address) external pure returns (bool) {
        return true; 
    }
}

contract Setup {
    SantasFastLane public target;
    MockNiceList public niceList;

    constructor() payable {
        niceList = new MockNiceList();
        target = new SantasFastLane{value: 100 ether}(address(niceList));
    }

    function isSolved() external view returns (bool) {
        return address(target).balance == 0;
    }
}
