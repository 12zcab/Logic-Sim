module ttl_7483 (
    input wire pin_A1,   // Operand A Bit 1 (Least Significant)
    input wire pin_A2,   // Operand A Bit 2
    input wire pin_A3,   // Operand A Bit 3
    input wire pin_A4,   // Operand A Bit 4 (Most Significant)
    input wire pin_B1,   // Operand B Bit 1 (Least Significant)
    input wire pin_B2,   // Operand B Bit 2
    input wire pin_B3,   // Operand B Bit 3
    input wire pin_B4,   // Operand B Bit 4 (Most Significant)
    input wire pin_C0,   // Carry-In Input
    output reg pin_S1,   // Sum Output Bit 1
    output reg pin_S2,   // Sum Output Bit 2
    output reg pin_S3,   // Sum Output Bit 3
    output reg pin_S4,   // Sum Output Bit 4
    output reg pin_C4    // Carry-Out Output Bit 4
);

    reg [4:0] sum_extended; // Temporary tracking array for handling carry overflow bit

    always @(*) begin
        sum_extended = {pin_A4, pin_A3, pin_A2, pin_A1} + {pin_B4, pin_B3, pin_B2, pin_B1} + pin_C0;
        
        pin_S1 = sum_extended;
        pin_S2 = sum_extended;
        pin_S3 = sum_extended;
        pin_S4 = sum_extended;
        pin_C4 = sum_extended; // Extra MSB represents total arithmetic carry out
    end

endmodule