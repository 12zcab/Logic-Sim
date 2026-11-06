module ttl_7414 (
    input wire pin_1A,   // Schmitt Inverter 1 Input
    output reg pin_1Y,   // Schmitt Inverter 1 Output
    input wire pin_2A,   // Schmitt Inverter 2 Input
    output reg pin_2Y,   // Schmitt Inverter 2 Output
    input wire pin_3A,   // Schmitt Inverter 3 Input
    output reg pin_3Y,   // Schmitt Inverter 3 Output
    output reg pin_4Y,   // Schmitt Inverter 4 Output
    input wire pin_4A,   // Schmitt Inverter 4 Input
    output reg pin_5Y,   // Schmitt Inverter 5 Output
    input wire pin_5A,   // Schmitt Inverter 5 Input
    output reg pin_6Y,   // Schmitt Inverter 6 Output
    input wire pin_6A    // Schmitt Inverter 6 Input
);

    always @(*) begin
        pin_1Y = ~pin_1A;
        pin_2Y = ~pin_2A;
        pin_3Y = ~pin_3A;
        pin_4Y = ~pin_4A;
        pin_5Y = ~pin_5A;
        pin_6Y = ~pin_6A;
    end

endmodule

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
