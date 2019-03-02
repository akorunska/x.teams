pragma solidity ^0.4.18;

contract SendFunds {
    function () public payable {}


    // 0x1137c1a1eeb22e507b21822827142ed4fd67d711
    function destuct (address instanceAddress) public {
        selfdestruct(instanceAddress);
    }
}