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