import "./LockedTransferringERC20.sol";
import "./Managed.sol";
import "./Shitcoin.sol";

pragma solidity ^0.5.0;

contract ShitcoinICO is Shitcoin {
    enum Phase { None, PreSale, PreSaleEnded, ICO, PostICO, Over }
    Phase public phase = Phase.None;
    bool public privateSaleOngoing = false;

    uint public ICOStartTime;
    uint public ICOEndTime;

    uint public tokensIssuedForPrivateSale = 48000000;
    uint public tokensBoughtAtPrivateSale;
    uint public tokensIssuedForPreSale = 32000000;
    uint public tokensBoughtAtPreSale;
    uint public tokensIssuedForICOPhase1 = 60000000;
    uint public tokensBoughtAtICOPhase1;
    uint public tokensIssuedForICOPhase2 = 55000000;
    uint public tokensBoughtAtICOPhase2;
    uint public tokensIssuedForICOPhase3 = 50000000;
    uint public tokensBoughtAtICOPhase3;
    uint public tokensIssuedForPostICO = 55000000;
    uint public tokensBoughtAtPostICO;

    uint weiInEther = 10 ** 8;
    uint centsInUSD = 100;
    uint USDPerEth = 600;
    // al values below represent price in wei per one Shitcoin
    uint public privateSalePrice = (13 * weiInEther) / (centsInUSD * USDPerEth);
    uint public preSalePrice = (15 * weiInEther) / (centsInUSD * USDPerEth);
    uint public ICOPhase1Price = (17 * weiInEther) / (centsInUSD * USDPerEth);
    uint public ICOPhase2Price = (18 * weiInEther) / (centsInUSD * USDPerEth);
    uint public ICOPrice = (20 * weiInEther) / (centsInUSD * USDPerEth);


    // address payable public teamAddress;
    // uint public tokensReservedByTeam = 30000000;
    // uint public tokensClaimedByTeam;
    // address payable public seedInvestorAddress;
    // uint public tokensReservedBySeedInvestor = 20000000;
    // uint public tokensClaimedBySeedInvestor;
    // address payable public advisorAddress;
    // uint public tokensReservedByAdvisor = 50000000;
    // uint public tokensClaimedByAdvisor;
    // address payable public founderAddress;
    // uint public tokensReservedByFounder = 50000000;
    // uint public tokensClaimedByFounder;
    // address payable public reservedAddress;
    // uint public tokensReserved = 50000000;
    // uint public tokensClaimedFromReserved;


    constructor(address _fundKeeper) public  Shitcoin(_fundKeeper) {
        // Shitcoin(_fundKeeper);
    }

    function startPrivateSale() public onlyAdmin onlyActive {
        require(privateSaleOngoing == false);
        privateSaleOngoing = true;
    }

    function startPreSale() public onlyAdmin onlyActive {
        require(phase == Phase.None);
        phase = Phase.PreSale;
    }

    function endPreSale() public onlyAdmin onlyActive {
        require(phase == Phase.PreSale);
        phase = Phase.PreSaleEnded;
    }

    function startICO() public onlyAdmin onlyActive {
        require(phase == Phase.PreSaleEnded);
        phase = Phase.ICO;
        ICOStartTime = block.timestamp;
    }

    function endICO() public onlyAdmin onlyActive {
        require(phase == Phase.ICO);
        phase = Phase.Over;
        privateSaleOngoing = false;
        ICOEndTime = block.timestamp;
    }

    function setPrivateSalePrice(uint newPrivateSalePrice) public onlyAdmin onlyActive {
        require(newPrivateSalePrice != 0);
        privateSalePrice = newPrivateSalePrice;
    }

    function setPreSalePrice(uint newPrivateSalePrice) public onlyAdmin onlyActive {
        require(newPrivateSalePrice != 0);
        privateSalePrice = newPrivateSalePrice;
    }

    function setICOPhase1Price(uint newICOPhase1Price) public onlyAdmin onlyActive {
        require(newICOPhase1Price != 0);
        ICOPhase1Price = newICOPhase1Price;
    }

    function setICOPhase2Price(uint newICOPhase2Price) public onlyAdmin onlyActive {
        require(newICOPhase2Price != 0);
        ICOPhase2Price = newICOPhase2Price;
    }

    function setICOPrice(uint newICOPrice) public onlyAdmin onlyActive {
        require(newICOPrice != 0);
        ICOPrice = newICOPrice;
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
        return 4;
    }

    function getCurrentState() public view returns (string memory) {
        if (phase == Phase.None) {
            return "None";
        } else if (phase == Phase.PreSale) {
            return "PreSale";
        } else if (phase == Phase.PreSaleEnded) {
            return "PreSale ended";
        } else if (phase == Phase.ICO) {
            uint round = getICOPhase();
            if (round == 1) {
                return "ICO Phase1";
            } else if (round == 2) {
                return "ICO Phase2";
            } else if (round == 3) {
                return "ICO Phase3";
            }
            return "Post ICO";
        }
        return "Over";
    }

    function enableTokenTransfer() public onlyActive onlyOwner {
        require(phase == Phase.Over);
        super.enableTokenTransfer();
    }



    function _issueTokenForPrivateInvestor(address investor, uint weiAmount) internal {
        uint tokensBought = _issueToken(investor, weiAmount, privateSalePrice);

        require (tokensBought + tokensBoughtAtPrivateSale <= tokensIssuedForPrivateSale);
        tokensBoughtAtPrivateSale += tokensBought;
    }

    function _issueTokenForPresale(address investor, uint weiAmount) internal {
        uint tokensBought = _issueToken(investor, weiAmount, preSalePrice);

        require (tokensBought + tokensBoughtAtPreSale <= tokensIssuedForPreSale);
        tokensBoughtAtPreSale += tokensBought;
    }

    function _issueTokenForICO(address investor, uint weiAmount, uint ICOPhase) internal {
        uint tokensBought;

        if (ICOPhase == 1) {
            tokensBought = _issueToken(investor, weiAmount, ICOPhase1Price);
            require (tokensBoughtAtICOPhase1 + tokensBought <= tokensIssuedForICOPhase1);
            tokensBoughtAtICOPhase1 += tokensBought;
        } else if (ICOPhase == 2) {
            tokensBought = _issueToken(investor, weiAmount, ICOPhase2Price);
            require (tokensBoughtAtICOPhase2 + tokensBought <= tokensIssuedForICOPhase2);
            tokensBoughtAtICOPhase2 += tokensBought;
        } else if (ICOPhase == 3) {
            tokensBought = _issueToken(investor, weiAmount, ICOPrice);
            require (tokensBoughtAtICOPhase3 + tokensBought <= tokensIssuedForICOPhase3);
            tokensBoughtAtICOPhase3 += tokensBought;
        } else {
            tokensBought = _issueToken(investor, weiAmount, ICOPrice);
            require (tokensBoughtAtPostICO + tokensBought <= tokensIssuedForPostICO);
            tokensBoughtAtPostICO += tokensBought;
        }
    }

    function _invest(address investor, uint weiAmount) internal returns (uint) {
        if (privateSaleOngoing == true && isPrivateInvestor(investor)) {
            _issueTokenForPrivateInvestor(investor, weiAmount);
        } else if (phase == Phase.PreSale && isWhiteListed(investor)) {
            _issueTokenForPresale(investor, weiAmount);
        } else {
            uint ICOPhase = getICOPhase();

            require(ICOPhase != 0);
            _issueTokenForICO(investor, weiAmount, ICOPhase);
        }
    }

    function fallback() public payable onlyActive {
        address invesorAddress = msg.sender;
        uint amount = msg.value;

        _invest(invesorAddress, amount);
    }




    // function setTeamAddress(address adr) public onlyAdmin onlyActive {
    //     require(adr != address(0));
    //     teamAddress = address(uint160(adr));
    // }

    // function allocateTokensForTeam() public onlyAdmin onlyActive {
    //     require(phase == Phase.Over);
    //     require(tokensReservedByTeam != tokensClaimedByTeam);

    //     if (tokensClaimedByTeam < 20 * tokensReservedByTeam / 100) {
    //         _mint(teamAddress,  (20 * tokensReservedByTeam / 100));
    //         tokensClaimedByTeam += 20 * tokensReservedByTeam / 100;
    //     }
    //     if (now >= ICOEndTime + 6 minutes && tokensClaimedByTeam < 50 * tokensReservedByTeam / 100 ) {
    //         _mint(teamAddress,  (30 * tokensReservedByTeam / 100));
    //         tokensClaimedByTeam += 20 * tokensReservedByTeam / 100;
    //     }
    //     if (now >= ICOEndTime + 12 minutes && tokensClaimedByTeam < tokensReservedByTeam) {
    //         _mint(teamAddress, (50 * tokensReservedByTeam / 100));
    //          tokensClaimedByTeam += 50 * tokensReservedByTeam / 100;
    //     }
    // }

    // function setFounderAddress(address adr) public onlyAdmin onlyActive {
    //     require(adr != address(0));
    //     founderAddress = address(uint160(adr));
    // }

    // function allocateTokensForFounder() public onlyAdmin onlyActive {
    //     require(phase == Phase.Over);
    //     require(tokensReservedByFounder != tokensClaimedByFounder);

    //     if (tokensClaimedByFounder < 20 * tokensReservedByFounder / 100) {
    //         _mint(founderAddress,  (20 * tokensReservedByFounder / 100));
    //         tokensClaimedByFounder += 20 * tokensReservedByFounder / 100;
    //     }
    //     if (now >= ICOEndTime + 6 minutes && tokensClaimedByFounder < 50 * tokensReservedByFounder / 100 ) {
    //         _mint(founderAddress,  (30 * tokensReservedByFounder / 100));
    //         tokensClaimedByFounder += 20 * tokensReservedByFounder / 100;
    //     }
    //     if (now >= ICOEndTime + 12 minutes && tokensClaimedByFounder < tokensReservedByFounder) {
    //         _mint(founderAddress, (50 * tokensReservedByFounder / 100));
    //          tokensClaimedByFounder += 50 * tokensReservedByFounder / 100;
    //     }
    // }

    // function setReservedAddress(address adr) public onlyAdmin onlyActive {
    //     require(adr != address(0));
    //     reservedAddress = address(uint160(adr));
    // }

    // function allocateTokensReserved() public onlyAdmin onlyActive {
    //     require(phase == Phase.Over);
    //     require(tokensReserved != tokensClaimedFromReserved);

    //     _mint(reservedAddress, tokensReserved);
    //     tokensClaimedFromReserved = tokensReserved;
    // }

    // function setAdvisorAddress(address adr) public onlyAdmin onlyActive {
    //     require(adr != address(0));
    //     advisorAddress = address(uint160(adr));
    // }

    // function allocateTokensForAdvisor() public onlyAdmin onlyActive {
    //     require(phase == Phase.Over);
    //     require(tokensReservedByAdvisor != tokensClaimedByAdvisor);

    //     _mint(advisorAddress, tokensReservedByAdvisor);
    //     tokensClaimedByAdvisor = tokensReservedByAdvisor;
    // }

    // function setSeedInvestorAddress(address adr) public onlyAdmin onlyActive {
    //     require(adr != address(0));
    //     seedInvestorAddress = address(uint160(adr));
    // }

    // function allocateTokensForSeedInvestor() public onlyAdmin onlyActive {
    //     require(phase == Phase.Over);
    //     require(tokensReservedBySeedInvestor != tokensClaimedBySeedInvestor);

    //     _mint(seedInvestorAddress, tokensReservedBySeedInvestor);
    //     tokensClaimedBySeedInvestor = tokensReservedBySeedInvestor;
    // }
}
