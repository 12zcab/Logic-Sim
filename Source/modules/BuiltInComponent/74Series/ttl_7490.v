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