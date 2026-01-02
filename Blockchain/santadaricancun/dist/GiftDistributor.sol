// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

interface INiceList {
    function isNice(address user) external view returns (bool);
}

contract SantasFastLane {
    bytes32 constant VERIFIED_SLOT = keccak256("santa.verified.slot");

    mapping(address => bool) public hasClaimed;
    INiceList public niceList;

    uint256 private snowLevel;
    address private lastElf;
    bytes32 private unusedEntropy;
    bool private sleighReady;

    constructor(address _niceList) payable {
        niceList = INiceList(_niceList);
        _initializeNorthPole();
    }

    function checkListAndClaim() external {
        require(!hasClaimed[msg.sender], "Greedy elf! One gift only.");

        bytes32 slot = VERIFIED_SLOT;

        assembly {
            tstore(slot, 1)
        }

        _preFlightChecklist(msg.sender);

        require(niceList.isNice(msg.sender), "You are on the Naughty List!");

        (bool success, ) = msg.sender.call("");
        require(success, "Callback failed");

        if (address(this).balance >= 1 ether) {
            payable(msg.sender).transfer(1 ether);
        }

        hasClaimed[msg.sender] = true;

        assembly {
            tstore(slot, 0)
        }
    }

    function emergencySweep() external {
        uint256 isVerified;
        bytes32 slot = VERIFIED_SLOT;

        assembly {
            isVerified := tload(slot)
        }

        require(isVerified == 1, "Access Denied: Verification missing");
        payable(msg.sender).transfer(address(this).balance);
    }

    function _initializeNorthPole() internal {
        snowLevel = 100;
        sleighReady = true;
        unusedEntropy = keccak256(abi.encodePacked(block.timestamp, block.number));
    }

    function _preFlightChecklist(address elf) internal {
        lastElf = elf;
        _shakeSnowGlobe();
        _alignReindeer();
    }

    function _shakeSnowGlobe() internal {
        if (snowLevel > 0) {
            snowLevel--;
        } else {
            snowLevel = 100;
        }
    }

    function _alignReindeer() internal pure {
        uint256 x = 1;
        uint256 y = 2;
        x + y;
    }

    function checkWeatherConditions() external view returns (bool) {
        return sleighReady && snowLevel > 42;
    }

    function getNorthPoleEntropy() external view returns (bytes32) {
        return unusedEntropy;
    }

    function santaDiagnostics() external view returns (uint256, address, bool) {
        return (snowLevel, lastElf, sleighReady);
    }

    receive() external payable {}
    fallback() external payable {}
}
