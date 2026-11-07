module ttl_7447 (
    input wire pin_A,    // BCD Input Bit 0
    input wire pin_B,    // BCD Input Bit 1
    input wire pin_C,    // BCD Input Bit 2
    input wire pin_D,    // BCD Input Bit 3
    input wire pin_LT_BAR, // Lamp Test Input (Active-Low)
    input wire pin_BI_RBO_BAR, // Blanking Input / Ripple Blanking Output (Active-Low)
    input wire pin_RBI_BAR, // Ripple Blanking Input (Active-Low)
    output reg pin_a_BAR, // Segment a Output (Active-Low)
    output reg pin_b_BAR, // Segment b Output (Active-Low)
    output reg pin_c_BAR, // Segment c Output (Active-Low)
    output reg pin_d_BAR, // Segment d Output (Active-Low)
    output reg pin_e_BAR, // Segment e Output (Active-Low)
    output reg pin_f_BAR, // Segment f Output (Active-Low)
    output reg pin_g_BAR  // Segment g Output (Active-Low)
);

    reg [6:0] segments;

    always @(*) begin
        if (!pin_BI_RBO_BAR) begin
            segments = 7'b1111111; // Blank display
        end else if (!pin_LT_BAR) begin
            segments = 7'b0000000; // All segments ON
        end else if (!pin_RBI_BAR && ({pin_D, pin_C, pin_B, pin_A} == 4'd0)) begin
            segments = 7'b1111111; // Blank leading zero
        end else begin
            case ({pin_D, pin_C, pin_B, pin_A})
                4'd0:  segments = 7'b0000001; // 0
                4'd1:  segments = 7'b1001111; // 1
                4'd2:  segments = 7'b0010010; // 2
                4'd3:  segments = 7'b0000110; // 3
                4'd4:  segments = 7'b1001100; // 4
                4'd5:  segments = 7'b0100100; // 5
                4'd6:  segments = 7'b0100000; // 6
                4'd7:  segments = 7'b0001111; // 7
                4'd8:  segments = 7'b0000000; // 8
                4'd9:  segments = 7'b0000100; // 9
                default: segments = 7'b1111111; // Blank for invalid BCD
            endcase
        end

        pin_a_BAR = segments[6]; pin_b_BAR = segments[5]; pin_c_BAR = segments[4];
        pin_d_BAR = segments[3]; pin_e_BAR = segments[2]; pin_f_BAR = segments[1];
        pin_g_BAR = segments[0];
    end

endmodule