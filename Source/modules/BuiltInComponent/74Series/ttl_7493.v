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