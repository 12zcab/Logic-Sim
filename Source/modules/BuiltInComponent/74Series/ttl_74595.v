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