module IC7430 (
    input  [7:0] A,
    output       Y
);
    assign Y = ~(&A);
endmodule