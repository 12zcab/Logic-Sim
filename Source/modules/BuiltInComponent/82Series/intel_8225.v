module intel_8255 (
    input wire pin_RESET,     // Master Reset Input (Active-High)
    input wire pin_CS_BAR,    // Chip Select Input (Active-Low Module Enable)
    input wire pin_RD_BAR,    // Read Command Control Line (Active-Low)
    input wire pin_WR_BAR,    // Write Command Control Line (Active-Low)
    input wire pin_A0,        // Address Bus Select Input Bit 0
    input wire pin_A1,        // Address Bus Select Input Bit 1
    inout wire [7:0] pin_D,   // 8-Bit Bidirectional Processor Data Bus
    inout wire [7:0] pin_PA,  // Programmable Interface Port A Bus
    inout wire [7:0] pin_PB,  // Programmable Interface Port B Bus
    inout wire [7:0] pin_PC   // Programmable Interface Port C Bus
);

    reg [7:0] control_register; // Configuration register mapping pin directions
    reg [7:0] out_PA;
    reg [7:0] out_PB;
    reg [7:0] out_PC;

    // Decode configuration flags: 0 = Output Mode, 1 = Input Mode
    wire port_a_in;
    wire port_b_in;
    wire port_c_in;
    
    assign port_a_in = control_register[4]; 
    assign port_b_in = control_register[1]; 
    assign port_c_in = control_register[0]; 

    // Handle incoming data writes from the host microprocessor
    always @(posedge pin_WR_BAR or posedge pin_RESET) begin
        if (pin_RESET) begin
            control_register <= 8'h9B; // Default system state boots all ports as inputs
            out_PA <= 8'h00; out_PB <= 8'h00; out_PC <= 8'h00;
        end else if (!pin_CS_BAR) begin
            case ({pin_A1, pin_A0})
                2'b00: if (!port_a_in) out_PA <= pin_D;
                2'b01: if (!port_b_in) out_PB <= pin_D;
                2'b10: if (!port_c_in) out_PC <= pin_D;
                2'b11: if (pin_D[7])   control_register <= pin_D;
            endcase
        end
    end

    // Direct dynamic wire routing based on mode setup configurations
    assign pin_PA = (!port_a_in) ? out_PA : 8'hzz;
    assign pin_PB = (!port_b_in) ? out_PB : 8'hzz;
    assign pin_PC = (!port_c_in) ? out_PC : 8'hzz;

    // Feed port state voltages back onto data highway lines during CPU reads
    assign pin_D = (!pin_CS_BAR && !pin_RD_BAR) ? (
        ({pin_A1, pin_A0} == 2'b00) ? pin_PA :
        ({pin_A1, pin_A0} == 2'b01) ? pin_PB :
        ({pin_A1, pin_A0} == 2'b10) ? pin_PC : control_register
    ) : 8'hzz;

endmodule
