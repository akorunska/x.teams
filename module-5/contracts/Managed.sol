pragma solidity ^0.5.0;

import "./Ownable.sol";

contract Managed is Ownable {
    bool public isActive = false;
    mapping (address => bool) public admins;
    address public portal;
    mapping (address => bool) public whitelist;
    mapping (address => bool) public privatelist;

    modifier onlyActive() {
        require(isActive == true);
        _;
    }

    modifier onlyInactive() {
        require(isActive == false);
        _;
    }

    modifier onlyAdmin() {
        require(msg.sender == owner() || admins[msg.sender] == true);
        _;
    }

    modifier onlyPortal() {
        require(msg.sender == owner() || admins[msg.sender] == true || portal == msg.sender);
        _;
    }

    modifier onlyWhitelisted() {
        require(whitelist[msg.sender] == true);
        _;
    }

    modifier onlyPrivateInvestors() {
        require(privatelist[msg.sender] == true);
        _;
    }

    constructor() public {
        portal = msg.sender;
    }


    // Contract activation / deactivation logic

    function activateContract() public onlyOwner onlyInactive {
        isActive = true;
    }

    function deactivateContract() public onlyOwner onlyActive {
        isActive = false;
    }

    // Admin related logic

    function addAdmin(address newAdminAddress) public onlyOwner onlyActive {
        require(admins[newAdminAddress] == false);
        admins[newAdminAddress] = true;
    }

    function isAdmin(address possibleAdminAddress) public view returns (bool) {
        return admins[possibleAdminAddress];
    }

    function removeAdmin(address adminAddressToRemove) public onlyOwner onlyActive {
        require(admins[adminAddressToRemove] == true);
        admins[adminAddressToRemove] = false;
    }


    // Portal address logic

    function setPortalAddress(address newPortalAddress) public onlyAdmin onlyActive {
        portal = newPortalAddress;
    }


    // Whitelist logic

    function addToWhiteList(address newWhitelistedAddress) public onlyPortal onlyActive {
        require(whitelist[newWhitelistedAddress] == false);
        whitelist[newWhitelistedAddress] = true;
    }

    function isWhiteListed(address possibleWhitelistedAddress) public view returns (bool) {
        return whitelist[possibleWhitelistedAddress];
    }

    function removeFromWhiteList(address whitelistAddressToRemove) public onlyPortal onlyActive {
        require(whitelist[whitelistAddressToRemove] == true);
        whitelist[whitelistAddressToRemove] = false;
    }


    // Private investor list logic

    function addPrivateInvestor(address investor) public onlyPortal onlyActive {
        require(privatelist[investor] == false);
        privatelist[investor] = true;
    }

    function isPrivateInvestor(address investor) public view returns (bool) {
        return privatelist[investor];
    }

    function removePrivateInversor(address investor) public onlyPortal onlyActive {
        require(privatelist[investor] == true);
        privatelist[investor] = false;
    }

}
