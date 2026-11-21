module IC7474 (
    input  [1:0] D,
    input  [1:0] CLK,
    input  [1:0] PRE_BAR
    input  [1:0] CLR_BAR
    output [1:0] Q,
    output [1:0] Q_n
);
    reg [1:0] q_reg;

    assign Q   = q_reg;
    assign Q_BAR= ~q_reg;

    always @(posedge CLK or negedge PRE_BARor negedge CLR_n) begin
        if (!CLR_n)
            q_reg <= 1'b0;
        else if (!PRE_n)
            q_reg <= 1'b1;
        else
            q_reg <= D;
    end

    always @(posedge CLK or negedge PRE_BARor negedge CLR_n) begin
        if (!CLR_n)
            q_reg <= 1'b0;
        else if (!PRE_n)
            q_reg <= 1'b1;
        else
            q_reg <= D;
    end
endmodule