module IC74283 (
    input  [3:0] A,
    input  [3:0] B,
    input        C0,
    output [3:0] S,
    output       C4
);
    assign {C4, S} = A + B + C0;
endmodule