pragma solidity 0.4.24;

import "contracts/UFragments.sol";

contract TEST is UFragments {
    uint256 initial_totalSupply;
    address public deployer;
    address public user1 = 0x00a329c0648769a73afac7f9381e08fb43dbea40;
    address public user2 = 0x00a329c0648769a73afac7f9381e08fb43dbea50;
    address public policy = 0x00a329c0648769a73afac7f9381e08fb43dbea60;
    uint256 constant public INITIAL_SUPPLY = 50000000000000000;

    constructor() public {
        deployer = msg.sender;
        initialize(deployer);
        _monetaryPolicy = policy;
        transfer(user1, 750000000000);
        transfer(user2, 250000000000);
        initial_totalSupply = _totalSupply;
    }

    function other_user() internal returns (address) {
        if (msg.sender == user2) {
            return user1;
        } else {
            return user2;
        }
    }

    function echidna_balanceToZero() public returns (bool) {
        if(_gonBalances[msg.sender] == 0) {
            return true;
        }
        return balanceOf(msg.sender) != 0;
    }

    function echidna_no_burn() returns (bool) {
        return (_gonBalances[0x0] == 0);
    }

    function echidna_self_transfer() returns (bool) {
        uint balance = _gonBalances[msg.sender].div(_gonsPerFragment);
        return (transfer(msg.sender,balance));
    }

    function echidna_zero_transfer() returns (bool) {
        return (transfer(other_user(),0));
    }

    function echidna_gons_invariant() returns (bool) {
        return (_gonsPerFragment == TOTAL_GONS.div(_totalSupply));
    }
    
    function echidna_self_approve_and_self_transferFrom() returns (bool) {
        uint balance = _gonBalances[msg.sender].div(_gonsPerFragment);
        approve(msg.sender, 0);
        approve(msg.sender, balance);
        return (transferFrom(msg.sender,msg.sender,balance));
    }

    function echidna_self_approve_and_transferFrom() returns (bool) {
        uint balance = _gonBalances[msg.sender].div(_gonsPerFragment);
        approve(msg.sender, 0);
        approve(msg.sender, balance);
        return (transferFrom(msg.sender,other_user(),balance));
    }
}
