module IC7490 (
    input        CKA,
    input        CKB,
    input        R01,
    input        R02,
    input        R91,
    input        R92,
    output [3:0] Q
);
    reg       qa;
    reg [2:0] qbcd;
    wire      r0 = R01 & R02;
    wire      r9 = R91 & R92;

    assign Q = {qbcd, qa};

    always @(negedge CKA or posedge r0 or posedge r9) begin
        if (r9)
            qa <= 1'b1;
        else if (r0)
            qa <= 1'b0;
        else
            qa <= ~qa;
    end

    always @(negedge CKB or posedge r0 or posedge r9) begin
        if (r9)
            qbcd <= 3'b100;
        else if (r0)
            qbcd <= 3'b000;
        else if (qbcd == 3'b100)
            qbcd <= 3'b000;
        else
            qbcd <= qbcd + 3'b001;
    end
endmodule