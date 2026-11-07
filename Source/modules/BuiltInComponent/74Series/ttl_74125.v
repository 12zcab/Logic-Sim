module ttl_74125 (
    input wire pin_1G_BAR, // Buffer 1 Output Enable (Active-Low)
    input wire pin_1A,     // Buffer 1 Input Data
    output reg pin_1Y,     // Buffer 1 Tri-State Output
    input wire pin_2G_BAR, // Buffer 2 Output Enable (Active-Low)
    input wire pin_2A,     // Buffer 2 Input Data
    output reg pin_2Y,     // Buffer 2 Tri-State Output
    output reg pin_3Y,     // Buffer 3 Tri-State Output
    input wire pin_3A,     // Buffer 3 Input Data
    input wire pin_3G_BAR, // Buffer 3 Output Enable (Active-Low)
    output reg pin_4Y,     // Buffer 4 Tri-State Output
    input wire pin_4A,     // Buffer 4 Input Data
    input wire pin_4G_BAR  // Buffer 4 Output Enable (Active-Low)
);

    always @(*) begin
        pin_1Y = (!pin_1G_BAR) ? pin_1A : 1'bz;
        pin_2Y = (!pin_2G_BAR) ? pin_2A : 1'bz;
        pin_3Y = (!pin_3G_BAR) ? pin_3A : 1'bz;
        pin_4Y = (!pin_4G_BAR) ? pin_4A : 1'bz;
    end

endmodule