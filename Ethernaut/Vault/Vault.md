# Ethernaut - Level 8 - Vault

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Vault {
  bool public locked;
  bytes32 private password;

  constructor(bytes32 _password) public {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
```

Objectives:
```
Unlock the vault to pass the level!
```

I solved this challenge in two ways:

	- The easy one
	- The medium one

## First method

In order to unlock the vault, we need to get the password; luckily, it was passed to the constructor, so we are able to find it in the transaction that had deployed the contract (constructor arguments are added at the end of the bytecode).

Contract bytecode:

```
608060405234801561001057600080fd5b506040516101653803806101658339818101604052602081101561003357600080fd5b810190808051906020019092919050505060016000806101000a81548160ff021916908315150217905550806001819055505060f1806100746000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c8063cf309012146037578063ec9b5b3a146057575b600080fd5b603d6082565b604051808215151515815260200191505060405180910390f35b608060048036036020811015606b57600080fd5b81019080803590602001909291905050506094565b005b6000809054906101000a900460ff1681565b80600154141560b85760008060006101000a81548160ff0219169083151502179055505b5056fea264697066735822122089d8dcab0ee2a6e0d4b11a8b0624f50e782fb879a941ed2f1d39cad24fdf2b1c64736f6c63430006030033412076657279207374726f6e67207365637265742070617373776f7264203a29
```

The first part is the loader of our contract, and the last 32 bytes are the argument passed to the constructor -> 412076657279207374726f6e67207365637265742070617373776f7264203a29.

This is the hexadecimal representation of the string.


## Second method

Thanks to @TheZ3ro, I learned about the qiling framework; it supports the emulation of the EVM machine and we are able to insert hook functions on specific EVM opcodes.

So I tried to put a function hook on the EQ opcode, so that I could see the operands that it was comparing (similar to what you can do with LD_PRELOAD on an ELF binary to hook the strcmp function)

The result is the same :)

![comp](https://user-images.githubusercontent.com/80392368/165901419-963fe5cf-fb42-46af-8460-3b8408f1d4db.PNG)



Link to @TheZ3ro amazing blog post about reversing smart contracts: https://www.shielder.com/blog/2022/04/a-sneak-peek-into-smart-contracts-reversing-and-emulation/
