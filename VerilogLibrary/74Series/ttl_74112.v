module IC74112 (
    input  [1:0] J,
    input  [1:0] K,
    input  [1:0] CLK,
    input  [1:0] PRE_BAR
    input  [1:0] CLR_BAR
    output [1:0] Q,
    output [1:0] Q_n
);
    reg [1:0] q_reg;

    assign Q   = q_reg;
    assign Q_BAR= ~q_reg;

    always @(negedge CLK or negedge PRE_BARor negedge CLR_n) begin
        if (!CLR_n)
            q_reg <= 1'b0;
        else if (!PRE_n)
            q_reg <= 1'b1;
        else begin
            case ({J, K})
                2'b00: q_reg <= q_reg;
                2'b01: q_reg <= 1'b0;
                2'b10: q_reg <= 1'b1;
                2'b11: q_reg <= ~q_reg;
            endcase
        end
    end

    always @(negedge CLK or negedge PRE_BARor negedge CLR_n) begin
        if (!CLR_n)
            q_reg <= 1'b0;
        else if (!PRE_n)
            q_reg <= 1'b1;
        else begin
            case ({J, K})
                2'b00: q_reg <= q_reg;
                2'b01: q_reg <= 1'b0;
                2'b10: q_reg <= 1'b1;
                2'b11: q_reg <= ~q_reg;
            endcase
        end
    end
endmodule