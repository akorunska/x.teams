pragma solidity ^0.4.0;

contract AkorunskLevel {
    address public owner;

    function AkorunskLevel() public {
        owner = msg.sender;
    }

    function claimOwnership() public {
        owner = msg.sender;
    }
}
