pragma solidity ^0.4.18;

contract Sandbox {

    uint startValue = 20;

    function add(uint val) public view returns (uint) {
        return startValue + val;
    }

    function subtract(uint val) public view returns (uint) {
        return startValue - val;
    }
}

// 115792089237316195423570985008687907853269984665640564039457584007913100000000
