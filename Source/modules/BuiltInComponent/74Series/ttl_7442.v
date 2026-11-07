module ttl_7442 (
    input wire pin_A,    // BCD Input Bit 0 (Least Significant)
    input wire pin_B,    // BCD Input Bit 1
    input wire pin_C,    // BCD Input Bit 2
    input wire pin_D,    // BCD Input Bit 3 (Most Significant)
    output reg pin_Y0_BAR, // Decimal Output 0 (Active-Low)
    output reg pin_Y1_BAR, // Decimal Output 1 (Active-Low)
    output reg pin_Y2_BAR, // Decimal Output 2 (Active-Low)
    output reg pin_Y3_BAR, // Decimal Output 3 (Active-Low)
    output reg pin_Y4_BAR, // Decimal Output 4 (Active-Low)
    output reg pin_Y5_BAR, // Decimal Output 5 (Active-Low)
    output reg pin_Y6_BAR, // Decimal Output 6 (Active-Low)
    output reg pin_Y7_BAR, // Decimal Output 7 (Active-Low)
    output reg pin_Y8_BAR, // Decimal Output 8 (Active-Low)
    output reg pin_Y9_BAR  // Decimal Output 9 (Active-Low)
);

    always @(*) begin
        // Reset all outputs to high (inactive state)
        pin_Y0_BAR = 1'b1; pin_Y1_BAR = 1'b1; pin_Y2_BAR = 1'b1; pin_Y3_BAR = 1'b1;
        pin_Y4_BAR = 1'b1; pin_Y5_BAR = 1'b1; pin_Y6_BAR = 1'b1; pin_Y7_BAR = 1'b1;
        pin_Y8_BAR = 1'b1; pin_Y9_BAR = 1'b1;

        // Decode active state based on 4-bit value (invalid BCD values 10-15 leave all outputs high)
        case ({pin_D, pin_C, pin_B, pin_A})
            4'd0: pin_Y0_BAR = 1'b0;
            4'd1: pin_Y1_BAR = 1'b0;
            4'd2: pin_Y2_BAR = 1'b0;
            4'd3: pin_Y3_BAR = 1'b0;
            4'd4: pin_Y4_BAR = 1'b0;
            4'd5: pin_Y5_BAR = 1'b0;
            4'd6: pin_Y6_BAR = 1'b0;
            4'd7: pin_Y7_BAR = 1'b0;
            4'd8: pin_Y8_BAR = 1'b0;
            4'd9: pin_Y9_BAR = 1'b0;
            default: ; // Do nothing
        endcase
    end

endmodule







