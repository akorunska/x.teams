import "./LockedTransferringERC20.sol";
import "./Managed.sol";

pragma solidity ^0.5.0;

contract ShitcoinICO is Managed {
    enum Phase { None, PrivateSale, PreSale, ICOPhase1, ICOPhase2, ICOPhase3, Donations }


    address public shitcoinAddress;
    Phase public phase = Phase.None;

    constructor (address _tokenAddress) public {
        shitcoinAddress = _tokenAddress;
    }

}
