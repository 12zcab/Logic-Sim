module ttl_74138 (
    input wire pin_A,        // Address Input Bit 0
    input wire pin_B,        // Address Input Bit 1
    input wire pin_C,        // Address Input Bit 2
    input wire pin_G1,       // Enable Input 1 (Active-High)
    input wire pin_G2A_BAR,  // Enable Input 2A (Active-Low)
    input wire pin_G2B_BAR,  // Enable Input 2B (Active-Low)
    output reg pin_Y0_BAR,   // Decoder Output 0 (Active-Low)
    output reg pin_Y1_BAR,   // Decoder Output 1 (Active-Low)
    output reg pin_Y2_BAR,   // Decoder Output 2 (Active-Low)
    output reg pin_Y3_BAR,   // Decoder Output 3 (Active-Low)
    output reg pin_Y4_BAR,   // Decoder Output 4 (Active-Low)
    output reg pin_Y5_BAR,   // Decoder Output 5 (Active-Low)
    output reg pin_Y6_BAR,   // Decoder Output 6 (Active-Low)
    output reg pin_Y7_BAR    // Decoder Output 7 (Active-Low)
);

    reg enabled;

    always @(*) begin
        enabled = pin_G1 & (!pin_G2A_BAR) & (!pin_G2B_BAR);

        if (enabled) begin
            pin_Y0_BAR = !({pin_C, pin_B, pin_A} == 3'd0);
            pin_Y1_BAR = !({pin_C, pin_B, pin_A} == 3'd1);
            pin_Y2_BAR = !({pin_C, pin_B, pin_A} == 3'd2);
            pin_Y3_BAR = !({pin_C, pin_B, pin_A} == 3'd3);
            pin_Y4_BAR = !({pin_C, pin_B, pin_A} == 3'd4);
            pin_Y5_BAR = !({pin_C, pin_B, pin_A} == 3'd5);
            pin_Y6_BAR = !({pin_C, pin_B, pin_A} == 3'd6);
            pin_Y7_BAR = !({pin_C, pin_B, pin_A} == 3'd7);
        end else begin
            pin_Y0_BAR = 1'b1; pin_Y1_BAR = 1'b1; pin_Y2_BAR = 1'b1; pin_Y3_BAR = 1'b1;
            pin_Y4_BAR = 1'b1; pin_Y5_BAR = 1'b1; pin_Y6_BAR = 1'b1; pin_Y7_BAR = 1'b1;
        end
    end

endmodule