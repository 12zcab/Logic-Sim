module IC7442 (
    input  [3:0] A,
    output [9:0] Y
);
    assign Y = (A < 4'd10) ? ~(10'b0000000001 << A) : 10'b1111111111;
endmodule