# Ethernaut - Level 5 - Token

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {

  mapping(address => uint) balances;
  uint public totalSupply;

  constructor(uint _initialSupply) public {
    balances[msg.sender] = totalSupply = _initialSupply;
  }

  function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }

  function balanceOf(address _owner) public view returns (uint balance) {
    return balances[_owner];
  }
}
```

Objectives:
```
The goal of this level is for you to hack the basic token contract below.

You are given 20 tokens to start with and you will beat the level if you somehow manage to get your hands on any additional tokens. Preferably a very large amount of tokens.
```

This was another easy one.

The problem here is that the mapping balances uses a uint (unsigned integer) to store the supply.

In the transfer method, there is a check to see if we have enough tokens to complete the transaction.

However, by using an unsigned integer, the balances cannot ever be negative: if we subtract something from zero, the balances will get the highest positive value a uint can represent.

To exploit this, we need to transfer to a random address a value x > 20, so that our balance will get the highest positive value:

```
contract.tranfer(randomaddress, 21);
```

