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
