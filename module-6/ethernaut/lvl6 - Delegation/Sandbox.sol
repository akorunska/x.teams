pragma solidity ^0.4.18;

contract Sandbox {

    function hash_pwn() public pure returns (bytes4) {
        return bytes4(sha3("pwn()"));
    }
}
