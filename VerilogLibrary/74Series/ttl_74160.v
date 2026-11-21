module IC74160 (
    input        CLK,
    input        CLR_BAR
    input        LOAD_BAR
    input        ENP,
    input        ENT,
    input  [3:0] D,
    output [3:0] Q,
    output       RCO
);
    reg [3:0] q_reg;

    assign Q   = q_reg;
    assign RCO = (q_reg == 4'd9) && ENT;

    always @(posedge CLK or negedge CLR_n) begin
        if (!CLR_n)
            q_reg <= 4'd0;
        else if (!LOAD_n)
            q_reg <= D;
        else if (ENP && ENT) begin
            if (q_reg == 4'd9)
                q_reg <= 4'd0;
            else
                q_reg <= q_reg + 4'd1;
        end
    end
endmodule