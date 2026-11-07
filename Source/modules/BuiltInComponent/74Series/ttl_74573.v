module ttl_74573 (
    input wire pin_OE_BAR, // Output Enable Input (Active-Low)
    input wire pin_LE,     // Latch Enable Input (Active-High)
    input wire pin_D0,     // Data Input Bit 0
    input wire pin_D1,     // Data Input Bit 1
    input wire pin_D2,     // Data Input Bit 2
    input wire pin_D3,     // Data Input Bit 3
    input wire pin_D4,     // Data Input Bit 4
    input wire pin_D5,     // Data Input Bit 5
    input wire pin_D6,     // Data Input Bit 6
    input wire pin_D7,     // Data Input Bit 7
    output reg pin_Q0,     // Data Output Bit 0 (Tri-State)
    output reg pin_Q1,     // Data Output Bit 1 (Tri-State)
    output reg pin_Q2,     // Data Output Bit 2 (Tri-State)
    output reg pin_Q3,     // Data Output Bit 3 (Tri-State)
    output reg pin_Q4,     // Data Output Bit 4 (Tri-State)
    output reg pin_Q5,     // Data Output Bit 5 (Tri-State)
    output reg pin_Q6,     // Data Output Bit 6 (Tri-State)
    output reg pin_Q7      // Data Output Bit 7 (Tri-State)
);

    reg [7:0] internal_storage;

    always @(*) begin
        // Data passes into latch while Latch Enable sits high
        if (pin_LE) begin
            internal_storage = {pin_D7, pin_D6, pin_D5, pin_D4, pin_D3, pin_D2, pin_D1, pin_D0};
        end

        // Resolving Output States
        if (!pin_OE_BAR) begin
            pin_Q0 = internal_storage[0];
            pin_Q1 = internal_storage[1];
            pin_Q2 = internal_storage[2];
            pin_Q3 = internal_storage[3];
            pin_Q4 = internal_storage[4];
            pin_Q5 = internal_storage[5];
            pin_Q6 = internal_storage[6];
            pin_Q7 = internal_storage[7];
        end else begin
            pin_Q0 = 1'bz; pin_Q1 = 1'bz; pin_Q2 = 1'bz; pin_Q3 = 1'bz;
            pin_Q4 = 1'bz; pin_Q5 = 1'bz; pin_Q6 = 1'bz; pin_Q7 = 1'bz;
        end
    end

endmodule

