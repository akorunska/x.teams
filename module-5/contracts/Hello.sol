pragma solidity ^0.5.0;

contract Hello {
    string public message;

    constructor(string memory _message) public {
        message = _message;
    }
}
