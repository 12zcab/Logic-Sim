# Core Documentation

## object.py

#### object.py mainly features four circuit object in different level.

### Component
Contains IO and Update function to manage IO.
During Construction the IO Pins can be passed in form of Dictionary or Array.
Dictionary will become a BetterDict Object,and Array will be first transformed to be a Dictionary according to the IO Objects' names

### IO
Mainly consist of two parts:
1. Value
IOObject.Value attribute's Read and Write will be automatically handled to ensure that 1 Value can handle both output and input at anytime without affecting the execution (Older Version (<= 11th Sept 2026) require Value and ValueOld)
2. Connection
connect,disconnect,connectNet,disconnectNet handle connection modification for IO to IO and IO to Net.

It also support >> operator for connection IO to IO and IO to Net
So u can achieve something like this:
Obj1.IO1 >> Obj2.IO2 >> Obj3.IO3
CLEANNNNNNNN AS HECKKKKKK YYAYYYYYYYYYYYYYYYY

### Net
1. Add/Remove
Add or remove IO from Net (Will Not Auto Update the IO)
2. Update
Pull up every IO pin in the net if one is pulling up
3. prepareDelete
Erm yah just prepare for delete :|
4. destroyNet
Correctly totally clean a Net when a Net is no longer in use

### SimBox
1. commitChange
Update every IO Pin status after the update is proposed
2. update
Call every update() function for Objects(IO Pins) and Nets, then apply change with commitChange() function
3. expandNet
Automatically add Net to Simulation Box by looking for Nets that are not added but used. (Highly recommended before executing the SimBox)
4. addObject
erm welp :| self explainary