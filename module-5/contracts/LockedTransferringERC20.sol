import "./ERC20.sol";
import "./Managed.sol";

pragma solidity ^0.5.0;


contract LockedTransferringERC20 is ERC20, Managed {
    bool transferringEnabled;

    constructor () public {
        transferringEnabled = false;
    }

    // can only be called once
    function enableTokenTransfer() public onlyActive onlyOwner {
        transferringEnabled = true;
    }

    function transfer(address to, uint256 value) public onlyActive returns (bool) {
        require(transferringEnabled == true);
        return super.transfer(to, value);
    }

    function transferFrom(address from, address to, uint256 value) public onlyActive returns (bool) {
        require(transferringEnabled == true);
        return super.transferFrom(from, to, value);
    }
}