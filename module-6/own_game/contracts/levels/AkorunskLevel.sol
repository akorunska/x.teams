pragma solidity ^0.4.18;

contract AkorunskLevel {
    address public owner;

    function AkorunskLevel() public {
        owner = msg.sender;
    }

    function claimOwnership() public {
        require(this.balance != 0);
        owner = msg.sender;
    }

    function contractBalance() public view returns (uint) {
        return this.balance;
    }
}
