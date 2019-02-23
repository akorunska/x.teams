import "./LockedTransferringERC20.sol";
import "./Managed.sol";
import "./Shitcoin.sol";

pragma solidity ^0.5.0;

contract ShitcoinICO is Shitcoin {
    enum Phase { None, PrivateSale, PreSale, PreSaleEnded, ICO, PostICO, Over }
    Phase public phase = Phase.None;

    uint public ICOStartTime;

    constructor (address _tokenAddress) public {
    }

    function startPrivateSale() public onlyAdmin {
        require(phase == Phase.None, "Private Sale mode can not be initiated now.");
        phase = Phase.PrivateSale;
    }

    function startPreSale() public onlyAdmin {
        require(phase == Phase.PrivateSale, "Pre Sale can only be started right after Private Sale");
        phase = Phase.PreSale;
    }

    function endPreSale() public onlyAdmin {
        require(phase == Phase.PreSale, "Pre sale was not started");
        phase = Phase.PreSaleEnded;
    }

    function startICO() public onlyAdmin {
        require(phase == Phase.PreSaleEnded, "Pre Sale was not ended");
        phase = Phase.ICO;
        ICOStartTime = block.timestamp;
    }

    function endICO() public onlyAdmin {
        require(phase == Phase.ICO, "ICO is not active");
        phase = Phase.Over;
    }

    function getICOPhase() public view returns (uint) {
        if (phase != Phase.ICO) {
            return 0;
        } else if (now <= ICOStartTime + 3 minutes) {
            return 1;
        } else if (now <= ICOStartTime + 6 minutes) {
            return 2;
        } else if (now <= ICOStartTime + 9 minutes) {
            return 3;
        }
        phase = Phase.PostICO;
        return 4;
    }

    function enableTokenTransfer() public onlyOwner {
        require(phase == Phase.Over, "Token transferring can only be enabled after ICO is over");
        super.enableTokenTransfer();
    }


}
