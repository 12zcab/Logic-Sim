module IC7448 (
    input  [3:0] BCD,
    input        LT_BAR
    input        RBI_BAR
    inout        BI_RBO_BAR
    output [6:0] SEG
);
    reg [6:0] seg_int;
    wire      rbo_int;

    assign rbo_int  = !((BCD == 4'd0) && !RBI_BAR&& LT_n);
    assign BI_RBO_BAR= rbo_int ? 1'bz : 1'b0;
    assign SEG      = !BI_RBO_BAR? 7'b0000000 : seg_int;

    always @(*) begin
        if (!LT_n)
            seg_int = 7'b1111111;
        else begin
            case (BCD)
                4'd0:    seg_int = 7'b0111111;
                4'd1:    seg_int = 7'b0000110;
                4'd2:    seg_int = 7'b1011011;
                4'd3:    seg_int = 7'b1001111;
                4'd4:    seg_int = 7'b1100110;
                4'd5:    seg_int = 7'b1101101;
                4'd6:    seg_int = 7'b1111100;
                4'd7:    seg_int = 7'b0000111;
                4'd8:    seg_int = 7'b1111111;
                4'd9:    seg_int = 7'b1100111;
                4'd10:   seg_int = 7'b0011100;
                4'd11:   seg_int = 7'b0001101;
                4'd12:   seg_int = 7'b1000110;
                4'd13:   seg_int = 7'b0011111;
                4'd14:   seg_int = 7'b1011110;
                4'd15:   seg_int = 7'b0000000;
                default: seg_int = 7'b0000000;
            endcase
        end
    end
endmodule