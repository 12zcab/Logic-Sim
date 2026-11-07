module sig_8T95 (
    input wire pin_G_BAR, // Master Output Enable Control Line (Active-Low)
    input wire pin_A1,    // Buffer 1 Input Data Channel
    output reg pin_Y1,    // Buffer 1 Tri-State Data Output
    input wire pin_A2,    // Buffer 2 Input Data Channel
    output reg pin_Y2,    // Buffer 2 Tri-State Data Output
    input wire pin_A3,    // Buffer 3 Input Data Channel
    output reg pin_Y3,    // Buffer 3 Tri-State Data Output
    input wire pin_A4,    // Buffer 4 Input Data Channel
    output reg pin_Y4,    // Buffer 4 Tri-State Data Output
    input wire pin_A5,    // Buffer 5 Input Data Channel
    output reg pin_Y5,    // Buffer 5 Tri-State Data Output
    input wire pin_A6,    // Buffer 6 Input Data Channel
    output reg pin_Y6     // Buffer 6 Tri-State Data Output
);

    always @(*) begin
        pin_Y1 = (!pin_G_BAR) ? pin_A1 : 1'bz;
        pin_Y2 = (!pin_G_BAR) ? pin_A2 : 1'bz;
        pin_Y3 = (!pin_G_BAR) ? pin_A3 : 1'bz;
        pin_Y4 = (!pin_G_BAR) ? pin_A4 : 1'bz;
        pin_Y5 = (!pin_G_BAR) ? pin_A5 : 1'bz;
        pin_Y6 = (!pin_G_BAR) ? pin_A6 : 1'bz;
    end

endmodule