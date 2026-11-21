module IC74181 (
    input  [3:0] A,
    input  [3:0] B,
    input  [3:0] S,
    input        M,
    input        Cn,
    output [3:0] F,
    output       A_eq_B,
    output       P,
    output       G,
    output       Cn4
);
    reg [4:0] arith_res;
    reg [3:0] logic_res;

    assign F      = M ? logic_res : arith_res[3:0];
    assign Cn4    = arith_res[4];
    assign A_eq_B = (F == 4'b1111);
    assign P      = 1'b0;
    assign G      = 1'b0;

    always @(*) begin
        case (S)
            4'b0000: logic_res = ~A;
            4'b0001: logic_res = ~(A | B);
            4'b0010: logic_res = (~A) & B;
            4'b0011: logic_res = 4'b0000;
            4'b0100: logic_res = ~(A & B);
            4'b0101: logic_res = ~B;
            4'b0110: logic_res = A ^ B;
            4'b0111: logic_res = A & (~B);
            4'b1000: logic_res = (~A) | B;
            4'b1001: logic_res = ~(A ^ B);
            4'b1010: logic_res = B;
            4'b1011: logic_res = A & B;
            4'b1100: logic_res = 4'b1111;
            4'b1101: logic_res = A | (~B);
            4'b1110: logic_res = A | B;
            4'b1111: logic_res = A;
        endcase

        case (S)
            4'b0000: arith_res = {1'b0, A} + !Cn;
            4'b0001: arith_res = {1'b0, (A | B)} + !Cn;
            4'b0010: arith_res = {1'b0, (A | ~B)} + !Cn;
            4'b0011: arith_res = 5'b11111 + !Cn;
            4'b0100: arith_res = {1'b0, A} + {1'b0, (A & ~B)} + !Cn;
            4'b0101: arith_res = {1'b0, (A | B)} + {1'b0, (A & ~B)} + !Cn;
            4'b0110: arith_res = {1'b0, A} - {1'b0, B} - Cn;
            4'b0111: arith_res = {1'b0, (A & ~B)} - Cn;
            4'b1000: arith_res = {1'b0, A} + {1'b0, (A & B)} + !Cn;
            4'b1001: arith_res = {1'b0, A} + {1'b0, B} + !Cn;
            4'b1010: arith_res = {1'b0, (A | ~B)} + {1'b0, (A & B)} + !Cn;
            4'b1011: arith_res = {1'b0, (A & B)} - Cn;
            4'b1100: arith_res = {1'b0, A} + {1'b0, A} + !Cn;
            4'b1101: arith_res = {1'b0, (A | B)} + {1'b0, A} + !Cn;
            4'b1110: arith_res = {1'b0, (A | ~B)} + {1'b0, A} + !Cn;
            4'b1111: arith_res = {1'b0, A} - Cn;
        endcase
    end
endmodule