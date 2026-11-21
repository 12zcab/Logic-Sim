module sig_8T97 (
    input wire pin_1G_BAR, // Controls Buffers 1 through 4 (Active-Low Enable)
    input wire pin_2G_BAR, // Controls Buffers 5 and 6 (Active-Low Enable)
    input wire pin_A1,     // Buffer 1 Input Data
    output reg pin_Y1,     // Buffer 1 Tri-State Output
    input wire pin_A2,     // Buffer 2 Input Data
    output reg pin_Y2,     // Buffer 2 Tri-State Output
    input wire pin_A3,     // Buffer 3 Input Data
    output reg pin_Y3,     // Buffer 3 Tri-State Output
    input wire pin_A4,     // Buffer 4 Input Data
    output reg pin_Y4,     // Buffer 4 Tri-State Output
    input wire pin_A5,     // Buffer 5 Input Data
    output reg pin_Y5,     // Buffer 5 Tri-State Output
    input wire pin_A6,     // Buffer 6 Input Data
    output reg pin_Y6      // Buffer 6 Tri-State Output
);

    always @(*) begin
        // Group 1: First 4 Buffers managed by control line 1G_BAR
        pin_Y1 = (!pin_1G_BAR) ? pin_A1 : 1'bz;
        pin_Y2 = (!pin_1G_BAR) ? pin_A2 : 1'bz;
        pin_Y3 = (!pin_1G_BAR) ? pin_A3 : 1'bz;
        pin_Y4 = (!pin_1G_BAR) ? pin_A4 : 1'bz;

        // Group 2: Remaining 2 Buffers managed by control line 2G_BAR
        pin_Y5 = (!pin_2G_BAR) ? pin_A5 : 1'bz;
        pin_Y6 = (!pin_2G_BAR) ? pin_A6 : 1'bz;
    end

endmodule
