"""
create NAND1 NandGate("q")   
create NAND2 NandGate("qm")
create NAND3 NandGate("s")   
create NAND4 NandGate("r")
create NOT1 NotGate("dm")
create keyd keyboard_button("key1","d")
create keyc keyboard_button("key2","c")
NAND1.IO.Y >> NAND2.IO.A
NAND2.IO.Y >> NAND1.IO.A
NAND3.IO.Y >> NAND1.IO.B
NAND4.IO.Y >> NAND2.IO.B
keyc.IO.OUT >> NAND3.IO.A >> NAND4.IO.A
keyd.IO.OUT >> NAND3.IO.B >> NOT1.IO.A
NOT1.IO.Y >> NAND4.IO.B
create logger Logger("logger",["Q"],[NAND1.IO.Y])
"""

"""
create dff BasicDFF("DFFTest")
create keyd keyboard_button("key1","d")
create keyc keyboard_button("key2","c")
keyd.IO.OUT >> dff.IO.D
keyc.IO.OUT >> dff.IO.CLK
create logger Logger("logger",["IND","INC","D","C","Q"],[keyd.IO.OUT,keyc.IO.OUT,dff.IO.D,dff.IO.CLK,dff.IO.Q])
"""

"""
create dff PP0_DFF("DFFPPOTest")
create keyd keyboard_button("key1","d")
create keyc keyboard_button("key2","c")
create keyr keyboard_button("key3","r")
keyd.IO.OUT >> dff.IO.D
keyc.IO.OUT >> dff.IO.C
keyr.IO.OUT >> dff.IO.R
create logger Logger("logger",["IND","INC","INR","Q"],[keyd.IO.OUT,keyc.IO.OUT,keyr.IO.OUT,dff.IO.Q])

"""

from core import *
from modules.LogicGate import *

class BasicDFF(Module):
    def __init__(self, Name):
        Pin_D = IO("D")
        Pin_CLK = IO("CLK")
        Pin_Q = IO("Q")
        Pin_QM = IO("QM")
        ModuleIO = [Pin_D,Pin_CLK,Pin_Q,Pin_QM]
        NandQ = NandGate("QY")
        NandQM = NandGate("QMY")
        NandS = NandGate("SIn")
        NandR = NandGate("RIn")
        NotD = NotGate("DInv")
        Blocks = [NandQ,NandQM,NandS,NandR,NotD]
        NandQ.IO.Y >> NandQM.IO.A >> Pin_Q
        NandQM.IO.Y >> NandQ.IO.A >> Pin_QM
        NandS.IO.Y >> NandQ.IO.B
        NandR.IO.Y >> NandQM.IO.B
        Pin_CLK >> NandS.IO.A >> NandR.IO.A
        Pin_D >> NandS.IO.B >> NotD.IO.A
        NotD.IO.Y >> NandR.IO.B
        super().__init__(Name, ModuleIO, Blocks)

class PP0_DFF(Module):
    def __init__(self, Name):
        Pin_D = IO("D")
        Pin_CLK = IO("C")
        Pin_RST = IO("R")
        Pin_Q = IO("Q")
        Pin_QM = IO("QM")
        ModuleIO = [Pin_D, Pin_CLK, Pin_RST, Pin_Q, Pin_QM]
        NandQ = NandGate("QY")
        NandQM = NandGate("QMY")
        NandS = NandGate("SIn")
        NandR = NandGate("RIn")
        NotD = NotGate("DInv")
        NotRST = NotGate("RstInv")
        ResetAndQ = AndGate("ClearQ")
        Blocks = [NandQ, NandQM, NandS, NandR, NotD, NotRST, ResetAndQ]
        Pin_RST >> NotRST.IO.A
        NandQ.IO.Y >> ResetAndQ.IO.A
        NotRST.IO.Y >> ResetAndQ.IO.B
        ResetAndQ.IO.Y >> NandQM.IO.A >> Pin_Q 
        NandQM.IO.Y >> NandQ.IO.A >> Pin_QM
        NandS.IO.Y >> NandQ.IO.B
        NandR.IO.Y >> NandQM.IO.B
        Pin_CLK >> NandS.IO.A >> NandR.IO.A
        Pin_D >> NandS.IO.B >> NotD.IO.A
        NotD.IO.Y >> NandR.IO.B
        
        super().__init__(Name, ModuleIO, Blocks)
