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