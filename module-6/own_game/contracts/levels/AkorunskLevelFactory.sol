pragma solidity ^0.4.18;

import './base/Level.sol';
import './AkorunskLevel.sol';

contract AkorunskLevelFactory is Level {

    function createInstance(address _player) public payable returns (address) {
        _player;
        AkorunskLevel instance = new AkorunskLevel();
        return instance;
    }

    function validateInstance(address _instance, address _player) public returns (bool) {
        AkorunskLevel instance = AkorunskLevel(_instance);
        return instance.owner() == _player;
    }
}
