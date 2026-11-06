module ttl_7474 (
    input wire pin_1CLK,     // Flip-Flop 1 Clock Input (Active on posedge)
    input wire pin_1D,       // Flip-Flop 1 Data Input
    input wire pin_1CLR_BAR, // Flip-Flop 1 Clear Input (Active-Low)
    input wire pin_1PR_BAR,  // Flip-Flop 1 Preset Input (Active-Low)
    output reg pin_1Q,       // Flip-Flop 1 True Output
    output reg pin_1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire pin_2CLK,     // Flip-Flop 2 Clock Input (Active on posedge)
    input wire pin_2D,       // Flip-Flop 2 Data Input
    input wire pin_2CLR_BAR, // Flip-Flop 2 Clear Input (Active-Low)
    input wire pin_2PR_BAR,  // Flip-Flop 2 Preset Input (Active-Low)
    output reg pin_2Q,       // Flip-Flop 2 True Output
    output reg pin_2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Core Logic Loop
    always @(posedge pin_1CLK or negedge pin_1CLR_BAR or negedge pin_1PR_BAR) begin
        if (!pin_1CLR_BAR) begin
            pin_1Q     <= 1'b0;
            pin_1Q_BAR <= 1'b1;
        end else if (!pin_1PR_BAR) begin
            pin_1Q     <= 1'b1;
            pin_1Q_BAR <= 1'b0;
        end else begin
            pin_1Q     <= pin_1D;
            pin_1Q_BAR <= ~pin_1D;
        end
    end

    // Flip-Flop 2 Core Logic Loop
    always @(posedge pin_2CLK or negedge pin_2CLR_BAR or negedge pin_2PR_BAR) begin
        if (!pin_2CLR_BAR) begin
            pin_2Q     <= 1'b0;
            pin_2Q_BAR <= 1'b1;
        end else if (!pin_2PR_BAR) begin
            pin_2Q     <= 1'b1;
            pin_2Q_BAR <= 1'b0;
        end else begin
            pin_2Q     <= pin_2D;
            pin_2Q_BAR <= ~pin_2D;
        end
    end

endmodule

module ttl_7476 (
    input wire pin_1CLK,     // Flip-Flop 1 Clock Input (Pulse-triggered / posedge)
    input wire pin_1J,       // Flip-Flop 1 J-Input
    input wire pin_1K,       // Flip-Flop 1 K-Input
    input wire pin_1CLR_BAR, // Flip-Flop 1 Clear Input (Active-Low)
    input wire pin_1PR_BAR,  // Flip-Flop 1 Preset Input (Active-Low)
    output reg pin_1Q,       // Flip-Flop 1 True Output
    output reg pin_1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire pin_2CLK,     // Flip-Flop 2 Clock Input (Pulse-triggered / posedge)
    input wire pin_2J,       // Flip-Flop 2 J-Input
    input wire pin_2K,       // Flip-Flop 2 K-Input
    input wire pin_2CLR_BAR, // Flip-Flop 2 Clear Input (Active-Low)
    input wire pin_2PR_BAR,  // Flip-Flop 2 Preset Input (Active-Low)
    output reg pin_2Q,       // Flip-Flop 2 True Output
    output reg pin_2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Core JK Logic
    always @(posedge pin_1CLK or negedge pin_1CLR_BAR or negedge pin_1PR_BAR) begin
        if (!pin_1CLR_BAR) begin
            pin_1Q     <= 1'b0;
            pin_1Q_BAR <= 1'b1;
        end else if (!pin_1PR_BAR) begin
            pin_1Q     <= 1'b1;
            pin_1Q_BAR <= 1'b0;
        end else begin
            case ({pin_1J, pin_1K})
                2'b00: begin pin_1Q <= pin_1Q; pin_1Q_BAR <= pin_1Q_BAR; end // Hold
                2'b01: begin pin_1Q <= 1'b0;   pin_1Q_BAR <= 1'b1;       end // Reset
                2'b10: begin pin_1Q <= 1'b1;   pin_1Q_BAR <= 1'b0;       end // Set
                2'b11: begin pin_1Q <= ~pin_1Q; pin_1Q_BAR <= ~pin_1Q_BAR; end // Toggle
            endcase
        end
    end

    // Flip-Flop 2 Core JK Logic
    always @(posedge pin_2CLK or negedge pin_2CLR_BAR or negedge pin_2PR_BAR) begin
        if (!pin_2CLR_BAR) begin
            pin_2Q     <= 1'b0;
            pin_2Q_BAR <= 1'b1;
        end else if (!pin_2PR_BAR) begin
            pin_2Q     <= 1'b1;
            pin_2Q_BAR <= 1'b0;
        end else begin
            case ({pin_2J, pin_2K})
                2'b00: begin pin_2Q <= pin_2Q; pin_2Q_BAR <= pin_2Q_BAR; end // Hold
                2'b01: begin pin_2Q <= 1'b0;   pin_2Q_BAR <= 1'b1;       end // Reset
                2'b10: begin pin_2Q <= 1'b1;   pin_2Q_BAR <= 1'b0;       end // Set
                2'b11: begin pin_2Q <= ~pin_2Q; pin_2Q_BAR <= ~pin_2Q_BAR; end // Toggle
            endcase
        end
    end

endmodule

module ttl_74112 (
    input wire pin_1CLK_BAR, // Flip-Flop 1 Clock Input (Active on negedge)
    input wire pin_1J,       // Flip-Flop 1 J-Input
    input wire pin_1K,       // Flip-Flop 1 K-Input
    input wire pin_1CLR_BAR, // Flip-Flop 1 Clear Input (Active-Low)
    input wire pin_1PR_BAR,  // Flip-Flop 1 Preset Input (Active-Low)
    output reg pin_1Q,       // Flip-Flop 1 True Output
    output reg pin_1Q_BAR,   // Flip-Flop 1 Inverted Output
    input wire pin_2CLK_BAR, // Flip-Flop 2 Clock Input (Active on negedge)
    input wire pin_2J,       // Flip-Flop 2 J-Input
    input wire pin_2K,       // Flip-Flop 2 K-Input
    input wire pin_2CLR_BAR, // Flip-Flop 2 Clear Input (Active-Low)
    input wire pin_2PR_BAR,  // Flip-Flop 2 Preset Input (Active-Low)
    output reg pin_2Q,       // Flip-Flop 2 True Output
    output reg pin_2Q_BAR    // Flip-Flop 2 Inverted Output
);

    // Flip-Flop 1 Core Logic Loop (Negative Edge Clock Triggered)
    always @(negedge pin_1CLK_BAR or negedge pin_1CLR_BAR or negedge pin_1PR_BAR) begin
        if (!pin_1CLR_BAR) begin
            pin_1Q     <= 1'b0;
            pin_1Q_BAR <= 1'b1;
        end else if (!pin_1PR_BAR) begin
            pin_1Q     <= 1'b1;
            pin_1Q_BAR <= 1'b0;
        end else begin
            case ({pin_1J, pin_1K})
                2'b00: begin pin_1Q <= pin_1Q; pin_1Q_BAR <= pin_1Q_BAR; end
                2'b01: begin pin_1Q <= 1'b0;   pin_1Q_BAR <= 1'b1;       end
                2'b10: begin pin_1Q <= 1'b1;   pin_1Q_BAR <= 1'b0;       end
                2'b11: begin pin_1Q <= ~pin_1Q; pin_1Q_BAR <= ~pin_1Q_BAR; end
            endcase
        end
    end

    // Flip-Flop 2 Core Logic Loop (Negative Edge Clock Triggered)
    always @(negedge pin_2CLK_BAR or negedge pin_2CLR_BAR or negedge pin_2PR_BAR) begin
        if (!pin_2CLR_BAR) begin
            pin_2Q     <= 1'b0;
            pin_2Q_BAR <= 1'b1;
        end else if (!pin_2PR_BAR) begin
            pin_2Q     <= 1'b1;
            pin_2Q_BAR <= 1'b0;
        end else begin
            case ({pin_2J, pin_2K})
                2'b00: begin pin_2Q <= pin_2Q; pin_2Q_BAR <= pin_2Q_BAR; end
                2'b01: begin pin_2Q <= 1'b0;   pin_2Q_BAR <= 1'b1;       end
                2'b10: begin pin_2Q <= 1'b1;   pin_2Q_BAR <= 1'b0;       end
                2'b11: begin pin_2Q <= ~pin_2Q; pin_2Q_BAR <= ~pin_2Q_BAR; end
            endcase
        end
    end

endmodule

module ttl_74373 (
    input wire pin_OE_BAR, // Output Enable Input (Active-Low)
    input wire pin_LE,     // Latch Enable Input (Active-High / Transparent when High)
    input wire pin_1D,     // Data Input 1
    output reg pin_1Q,     // Data Output 1 (Tri-State)
    input wire pin_2D,     // Data Input 2
    output reg pin_2Q,     // Data Output 2 (Tri-State)
    input wire pin_3D,     // Data Input 3
    output reg pin_3Q,     // Data Output 3 (Tri-State)
    input wire pin_4D,     // Data Input 4
    output reg pin_4Q,     // Data Output 4 (Tri-State)
    input wire pin_5D,     // Data Input 5
    output reg pin_5Q,     // Data Output 5 (Tri-State)
    input wire pin_6D,     // Data Input 6
    output reg pin_6Q,     // Data Output 6 (Tri-State)
    input wire pin_7D,     // Data Input 7
    output reg pin_7Q,     // Data Output 7 (Tri-State)
    input wire pin_8D,     // Data Input 8
    output reg pin_8Q      // Data Output 8 (Tri-State)
);

    reg [7:0] internal_latch; // Internal memory storage representation

    always @(*) begin
        // When LE is high, the latch is transparent (outputs follow inputs)
        if (pin_LE) begin
            internal_latch = {pin_8D, pin_7D, pin_6D, pin_5D, pin_4D, pin_3D, pin_2D, pin_1D};
        end
        
        // Handle Tri-State Output Bus mapping based on OE status
        if (!pin_OE_BAR) begin
            pin_1Q = internal_latch[0];
            pin_2Q = internal_latch[1];
            pin_3Q = internal_latch[2];
            pin_4Q = internal_latch[3];
            pin_5Q = internal_latch[4];
            pin_6Q = internal_latch[5];
            pin_7Q = internal_latch[6];
            pin_8Q = internal_latch[7];
        end else begin
            pin_1Q = 1'bz; pin_2Q = 1'bz; pin_3Q = 1'bz; pin_4Q = 1'bz;
            pin_5Q = 1'bz; pin_6Q = 1'bz; pin_7Q = 1'bz; pin_8Q = 1'bz;
        end
    end

endmodule

module ttl_74573 (
    input wire pin_OE_BAR, // Output Enable Input (Active-Low)
    input wire pin_LE,     // Latch Enable Input (Active-High)
    input wire pin_D0,     // Data Input Bit 0
    input wire pin_D1,     // Data Input Bit 1
    input wire pin_D2,     // Data Input Bit 2
    input wire pin_D3,     // Data Input Bit 3
    input wire pin_D4,     // Data Input Bit 4
    input wire pin_D5,     // Data Input Bit 5
    input wire pin_D6,     // Data Input Bit 6
    input wire pin_D7,     // Data Input Bit 7
    output reg pin_Q0,     // Data Output Bit 0 (Tri-State)
    output reg pin_Q1,     // Data Output Bit 1 (Tri-State)
    output reg pin_Q2,     // Data Output Bit 2 (Tri-State)
    output reg pin_Q3,     // Data Output Bit 3 (Tri-State)
    output reg pin_Q4,     // Data Output Bit 4 (Tri-State)
    output reg pin_Q5,     // Data Output Bit 5 (Tri-State)
    output reg pin_Q6,     // Data Output Bit 6 (Tri-State)
    output reg pin_Q7      // Data Output Bit 7 (Tri-State)
);

    reg [7:0] internal_storage;

    always @(*) begin
        // Data passes into latch while Latch Enable sits high
        if (pin_LE) begin
            internal_storage = {pin_D7, pin_D6, pin_D5, pin_D4, pin_D3, pin_D2, pin_D1, pin_D0};
        end

        // Resolving Output States
        if (!pin_OE_BAR) begin
            pin_Q0 = internal_storage[0];
            pin_Q1 = internal_storage[1];
            pin_Q2 = internal_storage[2];
            pin_Q3 = internal_storage[3];
            pin_Q4 = internal_storage[4];
            pin_Q5 = internal_storage[5];
            pin_Q6 = internal_storage[6];
            pin_Q7 = internal_storage[7];
        end else begin
            pin_Q0 = 1'bz; pin_Q1 = 1'bz; pin_Q2 = 1'bz; pin_Q3 = 1'bz;
            pin_Q4 = 1'bz; pin_Q5 = 1'bz; pin_Q6 = 1'bz; pin_Q7 = 1'bz;
        end
    end

endmodule
