import os
from .compiler import *

TEST_REG_VERILOG = """module reg8bit (
    input wire clk,      // Clock signal
    input wire rst,      // Active-high reset
    input wire en,       // Write enable
    input wire [7:0] d,  // Data input
    output reg [7:0] q   // Data output
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            q <= 8'b0;
        end else if (en) begin
            q <= d;
        end
    end

endmodule
"""

def print_bus_state(mod, label="[PIN STATE]"):
    """Properly inspects and reads bus state AFTER a simulation tick completes."""
    d_val = 0
    q_val = 0
    d_bits = []
    q_bits = []

    for i in range(8):
        bit_d = mod.IO.get(f"d_{i}")
        bit_q = mod.IO.get(f"q_{i}")

        # Cast to integer safely, treating None/False as 0
        v_d = int(bit_d.Value) if (bit_d and bit_d.Value is not None) else 0
        v_q = int(bit_q.Value) if (bit_q and bit_q.Value is not None) else 0

        d_bits.append(str(v_d))
        q_bits.append(str(v_q))

        d_val |= (v_d & 1) << i
        q_val |= (v_q & 1) << i

    print(f"  {label} D = 0x{d_val:02X} (0b{''.join(reversed(d_bits))}) ==> Q = 0x{q_val:02X} (0b{''.join(reversed(q_bits))})")

def set_bus_value(mod, bus_prefix, value, bit_width=8):
    for i in range(bit_width):
        bit_val = (value >> i) & 1
        pin_key = f"{bus_prefix}_{i}"
        
        pin = None
        if hasattr(mod, "IO") and pin_key in mod.IO:
            pin = mod.IO[pin_key]
        elif hasattr(mod, "PinOutIOs") and pin_key in mod.PinOutIOs:
            pin = mod.PinOutIOs[pin_key]
            
        if pin:
            pin.Value = bit_val
            # FIX: Print bit_val or pin.futureValue because pin.Value won't update until sim.update()
            print(f"  [DEBUG] Successfully set {pin_key} = {bit_val} (Pending Commit)")
        else:
            print(f"  ❌ [DEBUG] Pin '{pin_key}' NOT FOUND!")


def launch_test():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    v_path = os.path.join(current_dir, "register.v")
    
    if not os.path.exists(v_path):
        print(f"[Setup] Generating sample '{v_path}'...")
        with open(v_path, "w") as f:
            f.write(TEST_REG_VERILOG)

    print(f"\n[1] Compiling: {v_path}")
    reg_module = compile_verilog_file_to_object(v_path)
    print(f"✅ Created VerilogModule: '{reg_module.Name}'")

    sim = SimBox(Objects=[reg_module])
    sim.expandNet()

    # 快捷控制引腳的輔助函數（自動兼容不同字典）
    def set_pin(name, val):
        target_dict = reg_module.IO if hasattr(reg_module, "IO") and name in reg_module.IO else getattr(reg_module, "PinOutIOs", {})
        if name in target_dict:
            target_dict[name].Value = val

    print("\n[2] Initializing Input Pins (clk=0, rst=0, en=1)...")
    set_pin("clk", 0)
    set_pin("rst", 0)
    set_pin("en", 1)
    set_bus_value(reg_module, "d", 0x00)
    sim.update()  # 提交初始化狀態
    print("State BEFORE Clock Edge:")
    print_bus_state(reg_module)

    print("\n[3] Step 1: Drive D = 0xA5 and Trigger Clock PosEdge...")
    # --- 1. Setup Phase: 讓 D=0xA5 在網路上穩定生效 ---
    set_bus_value(reg_module, "d", 0xA5)
    set_pin("clk", 0)
    sim.update()  # 這一拍讓 D 真正進入 _Value，此時 clk 依舊為 0

    # --- 2. Clock Edge Phase: 保持 D 穩定，拉高時鐘觸發 PosEdge ---
    set_bus_value(reg_module, "d", 0xA5)
    set_pin("clk", 1)
    sim.update()  # 這一拍觸發 DFF 採樣，並將鎖存的值提交到 Q
    print_bus_state(reg_module)

    print("\n[4] Step 2: Change D = 0x5B WITHOUT Clock PosEdge...")
    # 改變數據，但時鐘保持為 1（維持高電平，沒有上升沿觸發）
    set_bus_value(reg_module, "d", 0x5B)
    set_pin("clk", 1)
    sim.update()          
    print_bus_state(reg_module)

    print("\n[5] Step 3: Trigger Next Clock PosEdge (Latch D=0x5B -> Q)...")
    # --- 1. Prepare Phase: 先把時鐘拉低，為下一個上升沿做準備 ---
    set_bus_value(reg_module, "d", 0x5B)
    set_pin("clk", 0)
    sim.update()  # 這一拍時鐘變回 0，數據 0x5B 繼續在網路上保持穩定

    # --- 2. Clock Edge Phase: 拉高時鐘，產生第二個正邊沿 ---
    set_bus_value(reg_module, "d", 0x5B)
    set_pin("clk", 1)
    sim.update()  # 這一拍鎖存 0x5B 到 Q
    print_bus_state(reg_module)

if __name__ == "__main__":
    launch_test()
