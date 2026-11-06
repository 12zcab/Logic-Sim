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

module ttl_74151 (
    input wire pin_D0,       // Data Input Channel 0
    input wire pin_D1,       // Data Input Channel 1
    input wire pin_D2,       // Data Input Channel 2
    input wire pin_D3,       // Data Input Channel 3
    input wire pin_D4,       // Data Input Channel 4
    input wire pin_D5,       // Data Input Channel 5
    input wire pin_D6,       // Data Input Channel 6
    input wire pin_D7,       // Data Input Channel 7
    input wire pin_A,        // Select Input Bit 0
    input wire pin_B,        // Select Input Bit 1
    input wire pin_C,        // Select Input Bit 2
    input wire pin_STROBE,   // Strobe Enable Input (Active-Low)
    output reg pin_Y,        // Multiplexer Output
    output reg pin_W         // Inverted Multiplexer Output
);

    always @(*) begin
        if (pin_STROBE) begin
            pin_Y = 1'b0;
            pin_W = 1'b1;
        end else begin
            case ({pin_C, pin_B, pin_A})
                3'd0: pin_Y = pin_D0;
                3'd1: pin_Y = pin_D1;
                3'd2: pin_Y = pin_D2;
                3'd3: pin_Y = pin_D3;
                3'd4: pin_Y = pin_D4;
                3'd5: pin_Y = pin_D5;
                3'd6: pin_Y = pin_D6;
                3'd7: pin_Y = pin_D7;
                default: pin_Y = 1'b0;
            endcase
            pin_W = ~pin_Y;
        end
    end

endmodule

module ttl_74157 (
    input wire pin_A,        // Select Input (Low selects A inputs, High selects B inputs)
    input wire pin_STROBE,   // Strobe Input (Active-Low Enable)
    input wire pin_1A,       // Multiplexer 1 Source A Data
    input wire pin_1B,       // Multiplexer 1 Source B Data
    output reg pin_1Y,       // Multiplexer 1 Output
    input wire pin_2A,       // Multiplexer 2 Source A Data
    input wire pin_2B,       // Multiplexer 2 Source B Data
    output reg pin_2Y,       // Multiplexer 2 Output
    input wire pin_3A,       // Multiplexer 3 Source A Data
    input wire pin_3B,       // Multiplexer 3 Source B Data
    output reg pin_3Y,       // Multiplexer 3 Output
    input wire pin_4A,       // Multiplexer 4 Source A Data
    input wire pin_4B,       // Multiplexer 4 Source B Data
    output reg pin_4Y        // Multiplexer 4 Output
);

    always @(*) begin
        if (pin_STROBE) begin
            // Outputs are forced low when strobe is high (disabled)
            pin_1Y = 1'b0;
            pin_2Y = 1'b0;
            pin_3Y = 1'b0;
            pin_4Y = 1'b0;
        end else begin
            pin_1Y = (pin_A) ? pin_1B : pin_1A;
            pin_2Y = (pin_A) ? pin_2B : pin_2A;
            pin_3Y = (pin_A) ? pin_3B : pin_3A;
            pin_4Y = (pin_A) ? pin_4B : pin_4A;
        end
    end

endmodule
