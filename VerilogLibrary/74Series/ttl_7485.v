module IC7485 (
    input  [3:0] A,
    input  [3:0] B,
    input        I_A_gt_B,
    input        I_A_eq_B,
    input        I_A_lt_B,
    output       O_A_gt_B,
    output       O_A_eq_B,
    output       O_A_lt_B
);
    assign O_A_gt_B = (A > B) || ((A == B) && I_A_gt_B);
    assign O_A_eq_B = (A == B) && I_A_eq_B;
    assign O_A_lt_B = (A < B) || ((A == B) && I_A_lt_B);
endmodule