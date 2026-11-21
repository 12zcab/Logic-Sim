module IC74192 (
    input        UP,
    input        DOWN,
    input        CLR,
    input        LOAD_BAR
    input  [3:0] D,
    output [3:0] Q,
    output       CO_BAR
    output       BO_n
);
    reg [3:0] q_reg;

    assign Q    = q_reg;
    assign CO_BAR= !((q_reg == 4'd9) && !UP);
    assign BO_BAR= !((q_reg == 4'd0) && !DOWN);

    always @(posedge UP or posedge DOWN or posedge CLR or negedge LOAD_n) begin
        if (CLR)
            q_reg <= 4'd0;
        else if (!LOAD_n)
            q_reg <= D;
        else if (UP && DOWN) begin
            if (q_reg == 4'd9)
                q_reg <= 4'd0;
            else
                q_reg <= q_reg + 4'd1;
        end else if (!UP && DOWN) begin
            if (q_reg == 4'd0)
                q_reg <= 4'd9;
            else
                q_reg <= q_reg - 4'd1;
        end
    end
endmodule