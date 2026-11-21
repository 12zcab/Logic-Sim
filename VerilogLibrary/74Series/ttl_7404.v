module IC7404 (
    input  [5:0] A,
    output [5:0] Y
);
    assign Y = ~A;
endmodule