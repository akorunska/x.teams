import "./ERC20.sol";
import "./Ownable.sol";

pragma solidity ^0.5.0;


contract LockedTransferringERC20 is ERC20, Ownable {
    bool transferringEnabled = false;

    function enableTokenTransfer () public onlyOwner {
        transferringEnabled = true;
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(transferringEnabled == true);
        return super.transfer(to, value);
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(transferringEnabled == true);
        return super.transferFrom(from, to, value);
    }
}

