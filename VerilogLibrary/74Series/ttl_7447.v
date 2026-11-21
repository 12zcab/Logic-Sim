module IC7447 (
    input  [3:0] BCD,
    input        LT_BAR
    input        RBI_BAR
    inout        BI_RBO_BAR
    output [6:0] SEG_n
);
    reg [6:0] seg_int;
    wire      rbo_int;

    assign rbo_int  = !((BCD == 4'd0) && !RBI_BAR&& LT_n);
    assign BI_RBO_BAR= rbo_int ? 1'bz : 1'b0;
    assign SEG_BAR   = !BI_RBO_BAR? 7'b1111111 : seg_int;

    always @(*) begin
        if (!LT_n)
            seg_int = 7'b0000000;
        else begin
            case (BCD)
                4'd0:    seg_int = 7'b1000000;
                4'd1:    seg_int = 7'b1111001;
                4'd2:    seg_int = 7'b0100100;
                4'd3:    seg_int = 7'b0110000;
                4'd4:    seg_int = 7'b0011001;
                4'd5:    seg_int = 7'b0010010;
                4'd6:    seg_int = 7'b0000011;
                4'd7:    seg_int = 7'b1111000;
                4'd8:    seg_int = 7'b0000000;
                4'd9:    seg_int = 7'b0011000;
                4'd10:   seg_int = 7'b1100011;
                4'd11:   seg_int = 7'b1110010;
                4'd12:   seg_int = 7'b0111001;
                4'd13:   seg_int = 7'b1100000;
                4'd14:   seg_int = 7'b0100001;
                4'd15:   seg_int = 7'b1111111;
                default: seg_int = 7'b1111111;
            endcase
        end
    end
endmodule