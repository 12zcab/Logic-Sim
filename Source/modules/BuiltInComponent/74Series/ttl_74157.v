module ttl_74157 (
    input wire pin_A,        // Select Input (Low selects A inputs, High selects B inputs)
    input wire pin_STROBE,   // Strobe Input (Active-Low Enable)
    input wire pin_1A,       // Multiplexer 1 Source A Data
    input wire pin_1B,       // Multiplexer 1 Source B Data
    output reg pin_1Y,       // Multiplexer 1 Output
    input wire pin_2A,       // Multiplexer 2 Source A Data
    input wire pin_2B,       // Multiplexer 2 Source B Data
    output reg pin_2Y,       // Multiplexer 2 Output
    input wire pin_3A,       // Multiplexer 3 Source A Data
    input wire pin_3B,       // Multiplexer 3 Source B Data
    output reg pin_3Y,       // Multiplexer 3 Output
    input wire pin_4A,       // Multiplexer 4 Source A Data
    input wire pin_4B,       // Multiplexer 4 Source B Data
    output reg pin_4Y        // Multiplexer 4 Output
);

    always @(*) begin
        if (pin_STROBE) begin
            // Outputs are forced low when strobe is high (disabled)
            pin_1Y = 1'b0;
            pin_2Y = 1'b0;
            pin_3Y = 1'b0;
            pin_4Y = 1'b0;
        end else begin
            pin_1Y = (pin_A) ? pin_1B : pin_1A;
            pin_2Y = (pin_A) ? pin_2B : pin_2A;
            pin_3Y = (pin_A) ? pin_3B : pin_3A;
            pin_4Y = (pin_A) ? pin_4B : pin_4A;
        end
    end

endmodule
