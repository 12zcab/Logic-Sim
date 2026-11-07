module ttl_7448 (
    input wire pin_A,    // BCD Input Bit 0
    input wire pin_B,    // BCD Input Bit 1
    input wire pin_C,    // BCD Input Bit 2
    input wire pin_D,    // BCD Input Bit 3
    input wire pin_LT_BAR, // Lamp Test Input (Active-Low)
    input wire pin_BI_RBO_BAR, // Blanking Input / Ripple Blanking Output (Active-Low)
    input wire pin_RBI_BAR, // Ripple Blanking Input (Active-Low)
    output reg pin_a,    // Segment a Output (Active-High)
    output reg pin_b,    // Segment b Output (Active-High)
    output reg pin_c,    // Segment c Output (Active-High)
    output reg pin_d,    // Segment d Output (Active-High)
    output reg pin_e,    // Segment e Output (Active-High)
    output reg pin_f,    // Segment f Output (Active-High)
    output reg pin_g     // Segment g Output (Active-High)
);

    reg [6:0] segments;

    always @(*) begin
        if (!pin_BI_RBO_BAR) begin
            segments = 7'b0000000; // Blank display
        end else if (!pin_LT_BAR) begin
            segments = 7'b1111111; // All segments ON
        end else if (!pin_RBI_BAR && ({pin_D, pin_C, pin_B, pin_A} == 4'd0)) begin
            segments = 7'b0000000; // Blank leading zero
        end else begin
            case ({pin_D, pin_C, pin_B, pin_A})
                4'd0:  segments = 7'b1111110; // 0
                4'd1:  segments = 7'b0110000; // 1
                4'd2:  segments = 7'b1101101; // 2
                4'd3:  segments = 7'b1111001; // 3
                4'd4:  segments = 7'b0110011; // 4
                4'd5:  segments = 7'b1011011; // 5
                4'd6:  segments = 7'b1011111; // 6
                4'd7:  segments = 7'b1110000; // 7
                4'd8:  segments = 7'b1111111; // 8
                4'd9:  segments = 7'b1111011; // 9
                default: segments = 7'b0000000; // Blank for invalid BCD
            endcase
        end

        pin_a = segments[6]; pin_b = segments[5]; pin_c = segments[4];
        pin_d = segments[3]; pin_e = segments[2]; pin_f = segments[1];
        pin_g = segments[0];
    end

endmodule