module ttl_7490 (
    input wire pin_CLKA,     // Clock Input A (Divide-by-2 section clock, negedge)
    input wire pin_CLKB,     // Clock Input B (Divide-by-5 section clock, negedge)
    input wire pin_R0_1,     // Reset-to-Zero Control Input 1
    input wire pin_R0_2,     // Reset-to-Zero Control Input 2
    input wire pin_R9_1,     // Reset-to-Nine Control Input 1
    input wire pin_R9_2,     // Reset-to-Nine Control Input 2
    output reg pin_QA,       // Counter Output Bit A
    output reg pin_QB,       // Counter Output Bit B
    output reg pin_QC,       // Counter Output Bit C
    output reg pin_QD        // Counter Output Bit D
);

    wire reset_to_zero;
    wire reset_to_nine;
    
    assign reset_to_zero = pin_R0_1 & pin_R0_2;
    assign reset_to_nine = pin_R9_1 & pin_R9_2;

    // Divide-by-2 Section Logic
    always @(negedge pin_CLKA or posedge reset_to_zero or posedge reset_to_nine) begin
        if (reset_to_zero) begin
            pin_QA <= 1'b0;
        end else if (reset_to_nine) begin
            pin_QA <= 1'b1;
        end else begin
            pin_QA <= ~pin_QA;
        end
    end

    // Divide-by-5 Section Logic
    reg [2:0] div5_count;
    always @(negedge pin_CLKB or posedge reset_to_zero or posedge reset_to_nine) begin
        if (reset_to_zero) begin
            div5_count <= 3'd0;
        end else if (reset_to_nine) begin
            div5_count <= 3'd4; // For BCD representation, 9 means div-by-5 stage is at state 4
        end else begin
            if (div5_count >= 3'd4) begin
                div5_count <= 3'd0;
            end else begin
                div5_count <= div5_count + 3'd1;
            end
        end
    end

    // Direct mapping to preserve internal register tracking
    always @(*) begin
        case (div5_count)
            3'd0: begin pin_QB = 1'b0; pin_QC = 1'b0; pin_QD = 1'b0; end
            3'd1: begin pin_QB = 1'b1; pin_QC = 1'b0; pin_QD = 1'b0; end
            3'd2: begin pin_QB = 1'b0; pin_QC = 1'b1; pin_QD = 1'b0; end
            3'd3: begin pin_QB = 1'b1; pin_QC = 1'b1; pin_QD = 1'b0; end
            3'd4: begin pin_QB = 1'b0; pin_QC = 1'b0; pin_QD = 1'b1; end
            default: begin pin_QB = 1'b0; pin_QC = 1'b0; pin_QD = 1'b0; end
        endcase
    end

endmodule

module ttl_7493 (
    input wire pin_CLKA,     // Clock Input A (Drives Stage A, active on negedge)
    input wire pin_CLKB,     // Clock Input B (Drives Stage B-C-D, active on negedge)
    input wire pin_R0_1,     // Master Reset Input 1 (Active-High)
    input wire pin_R0_2,     // Master Reset Input 2 (Active-High)
    output reg pin_QA,       // Counter Output Bit A
    output reg pin_QB,       // Counter Output Bit B
    output reg pin_QC,       // Counter Output Bit C
    output reg pin_QD        // Counter Output Bit D
);

    wire master_reset;
    assign master_reset = pin_R0_1 & pin_R0_2;

    // Stage A Ripple Logic Block
    always @(negedge pin_CLKA or posedge master_reset) begin
        if (master_reset) begin
            pin_QA <= 1'b0;
        end else begin
            pin_QA <= ~pin_QA;
        end
    end

    // Stages B, C, D Multi-stage Ripple Chain Logic
    reg [2:0] r_bcd;
    always @(negedge pin_CLKB or posedge master_reset) begin
        if (master_reset) begin
            r_bcd <= 3'd0;
        end else begin
            r_bcd <= r_bcd + 3'd1;
        end
    end

    always @(*) begin
        pin_QB = r_bcd;
        pin_QC = r_bcd;
        pin_QD = r_bcd;
    end

endmodule

module ttl_74160 (
    input wire pin_CLK,      // Clock Input (Active on posedge)
    input wire pin_CLR_BAR,  // Master Reset Clear Input (Asynchronous, Active-Low)
    input wire pin_LOAD_BAR, // Parallel Load Enable Input (Synchronous, Active-Low)
    input wire pin_ENP,      // Counting Enable Parallel Input (Active-High)
    input wire pin_ENT,      // Counting Enable Trickle Input (Active-High, drives RCO)
    input wire pin_A,        // Parallel Data Input Bit A
    input wire pin_B,        // Parallel Data Input Bit B
    input wire pin_C,        // Parallel Data Input Bit C
    input wire pin_D,        // Parallel Data Input Bit D
    output reg pin_QA,       // Counter Output Bit A
    output reg pin_QB,       // Counter Output Bit B
    output reg pin_QC,       // Counter Output Bit C
    output reg pin_QD,       // Counter Output Bit D
    output reg pin_RCO       // Ripple Carry Output (Terminal count sentinel)
);

    reg [3:0] count;

    always @(posedge pin_CLK or negedge pin_CLR_BAR) begin
        if (!pin_CLR_BAR) begin
            count <= 4'd0;
        end else begin
            if (!pin_LOAD_BAR) begin
                count <= {pin_D, pin_C, pin_B, pin_A};
            end else if (pin_ENP && pin_ENT) begin
                if (count >= 4'd9) begin
                    count <= 4'd0;
                end else begin
                    count <= count + 4'd1;
                end
            end
        end
    end

    always @(*) begin
        pin_QA = count;
        pin_QB = count;
        pin_QC = count;
        pin_QD = count;
        pin_RCO = (count == 4'd9) && pin_ENT;
    end

endmodule

module ttl_74161 (
    input wire pin_CLK,      // Clock Input (Active on posedge)
    input wire pin_CLR_BAR,  // Master Reset Clear Input (Asynchronous, Active-Low)
    input wire pin_LOAD_BAR, // Parallel Load Enable Input (Synchronous, Active-Low)
    input wire pin_ENP,      // Counting Enable Parallel Input (Active-High)
    input wire pin_ENT,      // Counting Enable Trickle Input (Active-High)
    input wire pin_A,        // Parallel Data Input Bit A
    input wire pin_B,        // Parallel Data Input Bit B
    input wire pin_C,        // Parallel Data Input Bit C
    input wire pin_D,        // Parallel Data Input Bit D
    output reg pin_QA,       // Counter Output Bit A
    output reg pin_QB,       // Counter Output Bit B
    output reg pin_QC,       // Counter Output Bit C
    output reg pin_QD,       // Counter Output Bit D
    output reg pin_RCO       // Ripple Carry Output (Active-High terminal flag)
);

    reg [3:0] count;

    always @(posedge pin_CLK or negedge pin_CLR_BAR) begin
        if (!pin_CLR_BAR) begin
            count <= 4'd0;
        end else begin
            if (!pin_LOAD_BAR) begin
                count <= {pin_D, pin_C, pin_B, pin_A};
            end else if (pin_ENP && pin_ENT) begin
                count <= count + 4'd1;
            end
        end
    end

    always @(*) begin
        pin_QA = count;
        pin_QB = count;
        pin_QC = count;
        pin_QD = count;
        pin_RCO = (count == 4'd15) && pin_ENT;
    end

endmodule

module ttl_74192 (
    input wire pin_CLK_UP,   // Count Up Clock Input (Triggered on posedge)
    input wire pin_CLK_DN,   // Count Down Clock Input (Triggered on posedge)
    input wire pin_CLR,      // Clear Input (Synchronous Active-High Reset)
    input wire pin_LOAD_BAR, // Asynchronous Parallel Load Input (Active-Low)
    input wire pin_A,        // Parallel Data Input A
    input wire pin_B,        // Parallel Data Input B
    input wire pin_C,        // Parallel Data Input C
    input wire pin_D,        // Parallel Data Input D
    output reg pin_QA,       // Counter Output Bit A
    output reg pin_QB,       // Counter Output Bit B
    output reg pin_QC,       // Counter Output Bit C
    output reg pin_QD,       // Counter Output Bit D
    output reg pin_CO_BAR,   // Carry Output (Active-Low Terminal overflow)
    output reg pin_BO_BAR    // Borrow Output (Active-Low Terminal underflow)
);

    reg [3:0] count;

    always @(posedge pin_CLK_UP or posedge pin_CLK_DN or posedge pin_CLR or negedge pin_LOAD_BAR) begin
        if (pin_CLR) begin
            count <= 4'd0;
        end else if (!pin_LOAD_BAR) begin
            count <= {pin_D, pin_C, pin_B, pin_A};
        end else if (pin_CLK_UP) begin
            if (count >= 4'd9) begin
                count <= 4'd0;
            end else begin
                count <= count + 4'd1;
            end
        end else if (pin_CLK_DN) begin
            if (count == 4'd0) begin
                count <= 4'd9;
            end else begin
                count <= count - 4'd1;
            end
        end
    end

    always @(*) begin
        pin_QA = count;
        pin_QB = count;
        pin_QC = count;
        pin_QD = count;
        pin_CO_BAR = !(pin_CLK_UP && (count == 4'd9));
        pin_BO_BAR = !(pin_CLK_DN && (count == 4'd0));
    end

endmodule

module ttl_74193 (
    input wire pin_CLK_UP,   // Count Up Clock Input (Triggered on posedge)
    input wire pin_CLK_DN,   // Count Down Clock Input (Triggered on posedge)
    input wire pin_CLR,      // Clear Input (Active-High Reset)
    input wire pin_LOAD_BAR, // Asynchronous Parallel Load Input (Active-Low)
    input wire pin_A,        // Parallel Data Input A
    input wire pin_B,        // Parallel Data Input B
    input wire pin_C,        // Parallel Data Input C
    input wire pin_D,        // Parallel Data Input D
    output reg pin_QA,       // Counter Output Bit A
    output reg pin_QB,       // Counter Output Bit B
    output reg pin_QC,       // Counter Output Bit C
    output reg pin_QD,       // Counter Output Bit D
    output reg pin_CO_BAR,   // Carry Output (Active-Low overflow sentinel)
    output reg pin_BO_BAR    // Borrow Output (Active-Low underflow sentinel)
);

    reg [3:0] count;

    always @(posedge pin_CLK_UP or posedge pin_CLK_DN or posedge pin_CLR or negedge pin_LOAD_BAR) begin
        if (pin_CLR) begin
            count <= 4'd0;
        end else if (!pin_LOAD_BAR) begin
            count <= {pin_D, pin_C, pin_B, pin_A};
        end else if (pin_CLK_UP) begin
            count <= count + 4'd1;
        end else if (pin_CLK_DN) begin
            count <= count - 4'd1;
        end
    end

    always @(*) begin
        pin_QA = count;
        pin_QB = count;
        pin_QC = count;
        pin_QD = count;
        pin_CO_BAR = !(pin_CLK_UP && (count == 4'd15));
        pin_BO_BAR = !(pin_CLK_DN && (count == 4'd0));
    end

endmodule

module ttl_74595 (
    input wire pin_SER,      // Serial Data Input
    input wire pin_SRCLK,    // Shift Register Clock Input (Pushes data on posedge)
    input wire pin_RCLK,     // Storage Register Latch Clock Input (Updates Y outputs on posedge)
    input wire pin_SRCLR_BAR,// Shift Register Clear Input (Active-Low Reset)
    input wire pin_OE_BAR,   // Output Enable Input (Active-Low Tri-state Control)
    output reg pin_QA,       // Parallel Data Output Bit A
    output reg pin_QB,       // Parallel Data Output Bit B
    output reg pin_QC,       // Parallel Data Output Bit C
    output reg pin_QD,       // Parallel Data Output Bit D
    output reg pin_QE,       // Parallel Data Output Bit E
    output reg pin_QF,       // Parallel Data Output Bit F
    output reg pin_QG,       // Parallel Data Output Bit G
    output reg pin_QH,       // Parallel Data Output Bit H
    output reg pin_QH_SER    // Serial Cascade Output (For chaining multiple 74595s)
);

    reg [7:0] shift_reg;    // Internal serial shift matrix storage
    reg [7:0] latch_reg;    // Internal storage register update matrix

    // Stage 1: Async Clear and Shift Register Clock Processing Loop
    always @(posedge pin_SRCLK or negedge pin_SRCLR_BAR) begin
        if (!pin_SRCLR_BAR) begin
            shift_reg <= 8'd0;
        end else begin
            shift_reg <= {shift_reg[6:0], pin_SER}; // Left-shift array sequence updating input
        end
    end

    // Stage 2: Synchronous Parallel Storage Register Latch Control Loop
    always @(posedge pin_RCLK or negedge pin_SRCLR_BAR) begin
        if (!pin_SRCLR_BAR) begin
            latch_reg <= 8'd0;
        end else begin
            latch_reg <= shift_reg; // Parallel transfer of shift memory onto active buffer latch
        end
    end

    // Stage 3: Resolving Output Ports & Tri-state Control Drivers
    always @(*) begin
        pin_QH_SER = shift_reg[7]; // Cascade bit bypasses output enable logic gate

        if (!pin_OE_BAR) begin
            pin_QA = latch_reg[0];
            pin_QB = latch_reg[1];
            pin_QC = latch_reg[2];
            pin_QD = latch_reg[3];
            pin_QE = latch_reg[4];
            pin_QF = latch_reg[5];
            pin_QG = latch_reg[6];
            pin_QH = latch_reg[7];
        end else begin
            pin_QA = 1'bz; pin_QB = 1'bz; pin_QC = 1'bz; pin_QD = 1'bz;
            pin_QE = 1'bz; pin_QF = 1'bz; pin_QG = 1'bz; pin_QH = 1'bz;
        end
    end

endmodule
