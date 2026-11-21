module IC74165 (
    input        CLK,
    input        CLK_INH,
    input        SH_LD_BAR
    input        SER,
    input  [7:0] D,
    output       QH,
    output       QH_n
);
    reg [7:0] shift_reg;
    wire      clk_eff = CLK | CLK_INH;

    assign QH   = shift_reg[7];
    assign QH_BAR= ~shift_reg[7];

    always @(posedge clk_eff or negedge SH_LD_n) begin
        if (!SH_LD_n)
            shift_reg <= D;
        else
            shift_reg <= {shift_reg[6:0], SER};
    end
endmodule