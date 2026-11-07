module ttl_7404 (
    input wire 1A,       // Inverter 1 Input
    output reg 1Y,       // Inverter 1 Output
    input wire 2A,       // Inverter 2 Input
    output reg 2Y,       // Inverter 2 Output
    input wire 3A,       // Inverter 3 Input
    output reg 3Y,       // Inverter 3 Output
    input wire 4A,       // Inverter 4 Input
    output reg 4Y,       // Inverter 4 Output
    input wire 5A,       // Inverter 5 Input
    output reg 5Y,       // Inverter 5 Output
    input wire 6A,       // Inverter 6 Input
    output reg 6Y        // Inverter 6 Output
);

    always @(*) begin
        1Y = ~1A;
        2Y = ~2A;
        3Y = ~3A;
        4Y = ~4A;
        5Y = ~5A;
        6Y = ~6A;
    end

endmodule