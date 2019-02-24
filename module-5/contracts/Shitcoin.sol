pragma solidity ^0.5.0;

import "./LockedTransferringERC20.sol";

contract Shitcoin is LockedTransferringERC20 {
    mapping (address => uint) investedEther;
    address payable public fundKeeper;
    address[] public investors;

    constructor (address _fundKeeper) public {
        fundKeeper = address(uint160(_fundKeeper));
    }


    function _issueToken(address investor, uint weiAmount, uint price) internal returns (uint) {
        uint tokenAmount = weiAmount / price;
        require (tokenAmount != 0);

        _mint(investor, tokenAmount);
        if (investedEther[investor] == 0) {
            investors.push(investor);
        }
        investedEther[investor] += weiAmount;
        fundKeeper.transfer(weiAmount);

        return tokenAmount;
    }

    function trackdownInvestedEther(address investor) public view onlyAdmin returns (uint) {
        return investedEther[investor];
    }

    function revokeToken(address investor) public payable onlyAdmin onlyActive {
        _burn(investor, balanceOf(investor));

        address payable investorToPay =  address(uint160(investor));
        investorToPay.transfer(msg.value);
    }

    function changeFundKeeper(address newFundKeeper) public onlyAdmin onlyActive {
        require(newFundKeeper != address(0));
        fundKeeper = address(uint160(newFundKeeper));
    }

}