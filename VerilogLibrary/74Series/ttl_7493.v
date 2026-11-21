module IC7493 (
    input        CKA,
    input        CKB,
    input        R01,
    input        R02,
    output [3:0] Q
);
    reg       qa;
    reg [2:0] qbcd;
    wire      r0 = R01 & R02;

    assign Q = {qbcd, qa};

    always @(negedge CKA or posedge r0) begin
        if (r0)
            qa <= 1'b0;
        else
            qa <= ~qa;
    end

    always @(negedge CKB or posedge r0) begin
        if (r0)
            qbcd <= 3'b000;
        else
            qbcd <= qbcd + 3'b001;
    end
endmodule