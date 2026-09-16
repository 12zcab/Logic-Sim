module reg8bit (
    input wire clk,      // Clock signal
    input wire rst,      // Active-high reset
    input wire en,       // Write enable
    input wire [7:0] d,  // Data input
    output reg [7:0] q   // Data output
);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            q <= 8'b0;
        end else if (en) begin
            q <= d;
        end
    end

endmodule
