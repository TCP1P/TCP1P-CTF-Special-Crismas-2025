// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "./ElfHub.sol";
import "./SantaLending.sol";

contract Setup {
    ElfHub public hub;
    SantaLending public lending;
    address public santa = 0x5474547454745474547454745474547454745474;

    constructor() payable {
        hub = new ElfHub();
        lending = new SantaLending(address(hub));

        hub.deposit{value: 100 ether}();
        lending.cheat_setCollateral(santa, 100 ether);
    }

    function isSolved() external view returns (bool) {
        return lending.collateral(santa) == 0;
    }
}
