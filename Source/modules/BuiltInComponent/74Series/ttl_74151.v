module ttl_74151 (
    input wire pin_D0,       // Data Input Channel 0
    input wire pin_D1,       // Data Input Channel 1
    input wire pin_D2,       // Data Input Channel 2
    input wire pin_D3,       // Data Input Channel 3
    input wire pin_D4,       // Data Input Channel 4
    input wire pin_D5,       // Data Input Channel 5
    input wire pin_D6,       // Data Input Channel 6
    input wire pin_D7,       // Data Input Channel 7
    input wire pin_A,        // Select Input Bit 0
    input wire pin_B,        // Select Input Bit 1
    input wire pin_C,        // Select Input Bit 2
    input wire pin_STROBE,   // Strobe Enable Input (Active-Low)
    output reg pin_Y,        // Multiplexer Output
    output reg pin_W         // Inverted Multiplexer Output
);

    always @(*) begin
        if (pin_STROBE) begin
            pin_Y = 1'b0;
            pin_W = 1'b1;
        end else begin
            case ({pin_C, pin_B, pin_A})
                3'd0: pin_Y = pin_D0;
                3'd1: pin_Y = pin_D1;
                3'd2: pin_Y = pin_D2;
                3'd3: pin_Y = pin_D3;
                3'd4: pin_Y = pin_D4;
                3'd5: pin_Y = pin_D5;
                3'd6: pin_Y = pin_D6;
                3'd7: pin_Y = pin_D7;
                default: pin_Y = 1'b0;
            endcase
            pin_W = ~pin_Y;
        end
    end

endmodule

