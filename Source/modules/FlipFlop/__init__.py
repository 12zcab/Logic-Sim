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
        # 1. Declare IO objects
        Pin_D   = IO("D")
        Pin_CLK = IO("C")
        Pin_RST = IO("R")
        Pin_Q   = IO("Q")
        Pin_QM  = IO("QM")
        ModuleIO = [Pin_D, Pin_CLK, Pin_RST, Pin_Q, Pin_QM]

        # 2. Instantiate Internal Gates
        NotCLK   = NotGate("ClkInv")
        NotRST   = NotGate("RstInv")
        M_NandS  = NandGate("M_SIn")
        M_NandR  = NandGate("M_RIn")
        M_NotD   = NotGate("M_DInv")
        M_NandQ  = NandGate("M_QY")
        M_NandQM = NandGate3("M_QMY")
        S_NandS  = NandGate("S_SIn")
        S_NandR  = NandGate("S_RIn")
        S_NandQ  = NandGate("S_QY")
        S_NandQM = NandGate3("S_QMY")

        Blocks = [
            NotCLK, NotRST,
            M_NandS, M_NandR, M_NotD, M_NandQ, M_NandQM,
            S_NandS, S_NandR, S_NandQ, S_NandQM
        ]

        # 3. Register Module IOs with super() FIRST
        super().__init__(Name, ModuleIO, Blocks)

        # 4. Connect Input Ports using self.IO
        self.IO.C >> NotCLK.IO.A
        self.IO.R >> NotRST.IO.A

        # Master Latch Clocking & Data
        NotCLK.IO.Y >> M_NandS.IO.A
        NotCLK.IO.Y >> M_NandR.IO.A

        self.IO.D >> M_NandS.IO.B
        self.IO.D >> M_NotD.IO.A
        M_NotD.IO.Y >> M_NandR.IO.B

        M_NandS.IO.Y >> M_NandQ.IO.B
        M_NandR.IO.Y >> M_NandQM.IO.B

        # Master Latch Feedback & Reset Integration
        M_NandQ.IO.Y  >> M_NandQM.IO.A
        NotRST.IO.Y   >> M_NandQM.IO.C
        M_NandQM.IO.Y >> M_NandQ.IO.A

        # Slave Latch Clocking & Steering
        self.IO.C >> S_NandS.IO.A
        self.IO.C >> S_NandR.IO.A

        M_NandQ.IO.Y  >> S_NandS.IO.B
        M_NandQM.IO.Y >> S_NandR.IO.B

        S_NandS.IO.Y >> S_NandQ.IO.B
        S_NandR.IO.Y >> S_NandQM.IO.B

        # Slave Latch Feedback & Reset Integration
        S_NandQ.IO.Y  >> S_NandQM.IO.A
        NotRST.IO.Y   >> S_NandQM.IO.C
        S_NandQM.IO.Y >> S_NandQ.IO.A

        # 5. Connect Output Ports using self.IO
        S_NandQ.IO.Y  >> self.IO.Q
        S_NandQM.IO.Y >> self.IO.QM
        
        
        
def dff_behavioral_update(comp):
    curr_clk = comp.IO.C.Value
    rst_val  = comp.IO.R.Value
    d_val    = comp.IO.D.Value

    prev_clk = getattr(comp, "_prev_clk", Logic.ZERO)

    # Active High Reset
    if rst_val == Logic.ONE:
        comp.IO.Q.setPower(Logic.ZERO, strength=Strength.STRONG, Delay=0)
        comp.IO.QM.setPower(Logic.ONE, strength=Strength.STRONG, Delay=0)

    # Rising Edge Trigger (0 -> 1 transition)
    elif prev_clk == Logic.ZERO and curr_clk == Logic.ONE:
        if d_val in (Logic.ONE, Logic.ZERO):
            qm_val = Logic.ZERO if d_val == Logic.ONE else Logic.ONE
            comp.IO.Q.setPower(d_val, strength=Strength.STRONG, Delay=0)
            comp.IO.QM.setPower(qm_val, strength=Strength.STRONG, Delay=0)

    comp._prev_clk = curr_clk

class PP0_DFF_behave(Component):
    def __init__(self, Name):
        super().__init__(
            Name,
            [IO("D"), IO("C"), IO("R"), IO("Q"), IO("QM")],
            updateFunction=dff_behavioral_update
        )