# CLI
### DataLogger and LogicGates in CLI
```
create And AndGate("AND")
create Or OrGate("OR")
create Xor XorGate("XOR")
create a keyboard_button("ABT","a")
create b keyboard_button("BBT","b")
create log Logger("logger",["A","B","AND","OR","XOR"],[a.IO.OUT,b.IO.OUT,And.IO.Y,Or.IO.Y,Xor.IO.Y])
a.IO.OUT >> And.IO.A >> Or.IO.A >> Xor.IO.A
b.IO.OUT >> And.IO.B >> Or.IO.B >> Xor.IO.B
run 0.05
```
### Not Gate Pulse Signal,Error Handle.
```
asd
create notgate NotGate("Not")
create logger Logger("logger",["SignalIn","SignalOut"],[notgate.IO.A,notgate.IO.Y])
notgate.IO.A >> notgate.IO.B
notgate.IO.A >> notgate.IO.Y
run 0.01 5
```
Output:
```
>asd
Eval Error in [asd]: 
name 'asd' is not defined
Error
>create notgate NotGate("Not")
>create logger Logger("logger",["SignalIn","SignalOut"],[notgate.IO.A,notgate.IO.Y])
>notgate.IO.A >> notgate.IO.B
Eval Error in [varVault["notgate"].IO.A >> varVault["notgate"].IO.B]: 
'BetterDict' object has no attribute 'B'
Error
>notgate.IO.A >> notgate.IO.Y
<core.module.object.IO object at 0x0000023DB7E77250>
>run 0.01 5 
logger===0
+------------+-------------+
|   SignalIn |   SignalOut |
+============+=============+
|          0 |           0 |
+------------+-------------+
logger===1
+------------+-------------+
|   SignalIn |   SignalOut |
+============+=============+
|          1 |           1 |
+------------+-------------+
logger===2
+------------+-------------+
|   SignalIn |   SignalOut |
+============+=============+
|          0 |           0 |
+------------+-------------+
logger===3
+------------+-------------+
|   SignalIn |   SignalOut |
+============+=============+
|          1 |           1 |
+------------+-------------+
logger===4
+------------+-------------+
|   SignalIn |   SignalOut |
+============+=============+
|          0 |           0 |
+------------+-------------+
Average Tick Per Second:92.26420038735863
>
```
Though it may seem not correct as Not Gate's Input and Output is the same,but it actually reflects the truth status of a logic gate.With output and input shorted,its output and input MUST BE THE SAME,so the Not Gate is experiencing a process delay between ticks
So this actually simulate the real-world situation
### Verilog Import Test
```
create register parseFileIntoObject("register.v")
create clkbt keyboard_button("clk","[")
create rstbt keyboard_button("rst","]")
create enbt keyboard_button("en",'\\')
create d0 keyboard_button("d0","1")
create d1 keyboard_button("d1","2")
create d2 keyboard_button("d2","3")
create d3 keyboard_button("d3","4")
create d4 keyboard_button("d4","5")
create d5 keyboard_button("d5","6")
create d6 keyboard_button("d6","7")
create d7 keyboard_button("d7","8")
clkbt.IO.OUT >> register.IO.clk
rstbt.IO.OUT >> register.IO.rst
enbt.IO.OUT >> register.IO.en
d0.IO.OUT >> register.IO.d_0
d1.IO.OUT >> register.IO.d_1
d2.IO.OUT >> register.IO.d_2
d3.IO.OUT >> register.IO.d_3
d4.IO.OUT >> register.IO.d_4
d5.IO.OUT >> register.IO.d_5
d6.IO.OUT >> register.IO.d_6
d7.IO.OUT >> register.IO.d_7
create log Logger("logger", ["CLK", "RST", "EN", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"], [register.IO.clk, register.IO.rst, register.IO.en, register.IO.d_0, register.IO.d_1, register.IO.d_2, register.IO.d_3, register.IO.d_4, register.IO.d_5, register.IO.d_6, register.IO.d_7, register.IO.q_0, register.IO.q_1, register.IO.q_2, register.IO.q_3, register.IO.q_4, register.IO.q_5, register.IO.q_6, register.IO.q_7])
run 0
```
use [ as clk, ] as reset , and \ as enable and 12345678 as Data Bus to test a register imported from Verilog!!!!!