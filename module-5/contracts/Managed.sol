pragma solidity ^0.5.0;

import "./Ownable.sol";

contract Managed is Ownable {
    bool public isActive = false;
    mapping (address => bool) public admins;
    address portal;
    mapping (address => bool) public whitelist;
    mapping (address => bool) public privatelist;

    modifier onlyActive() {
        require(isActive == true, "Contract is not active right now.");
        _;
    }

    modifier onlyInactive() {
        require(isActive == false, "Contract is already active.");
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
        require(admins[newAdminAddress] == false, "This address is admin already.");
        admins[newAdminAddress] = true;
    }

    function isAdmin(address possibleAdminAddress) public view returns (bool) {
        return admins[possibleAdminAddress];
    }

    function removeAdmin(address adminAddressToRemove) public onlyOwner onlyActive {
        require(admins[adminAddressToRemove] == true, "This address does not belong to the admin");
        admins[adminAddressToRemove] = false;
    }


    // Portal address logic

    function setPortalAddress(address newPortalAddress) public onlyAdmin onlyActive {
        portal = newPortalAddress;
    }


    // Whitelist logic

    function addToWhiteList(address newWhitelistedAddress) public onlyPortal onlyActive {
        require(whitelist[newWhitelistedAddress] == false, "This address is whitelisted already.");
        whitelist[newWhitelistedAddress] = true;
    }

    function isWhiteListed(address possibleWhitelistedAddress) public view returns (bool) {
        return whitelist[possibleWhitelistedAddress];
    }

    function removeFromWhiteList(address whitelistAddressToRemove) public onlyPortal onlyActive {
        require(whitelist[whitelistAddressToRemove] == true, "This address is not on the whitelist");
        whitelist[whitelistAddressToRemove] = false;
    }


    // Private investor list logic

    function addPrivateInvestor(address investor) public onlyPortal onlyActive {
        require(privatelist[investor] == false, "This address is private investor already.");
        privatelist[investor] = true;
    }

    function isPrivateInvestor(address investor) public view returns (bool) {
        return privatelist[investor];
    }

    function removePrivateInversor(address investor) public onlyPortal onlyActive {
        require(privatelist[investor] == true, "This address does not belong to the private investor");
        privatelist[investor] = false;
    }

}
