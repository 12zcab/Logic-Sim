module ttl_7430 (
    input wire pin_A,    // Input Channel A
    input wire pin_B,    // Input Channel B
    input wire pin_C,    // Input Channel C
    input wire pin_D,    // Input Channel D
    input wire pin_E,    // Input Channel E
    input wire pin_F,    // Input Channel F
    input wire pin_G,    // Input Channel G
    input wire pin_H,    // Input Channel H
    output reg pin_Y     // Unified NAND Output Y
);
  
    always @(*) begin
        pin_Y = ~(pin_A & pin_B & pin_C & pin_D & pin_E & pin_F & pin_G & pin_H);
    end

endmodule