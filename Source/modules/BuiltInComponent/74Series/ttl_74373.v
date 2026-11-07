module ttl_74373 (
    input wire pin_OE_BAR, // Output Enable Input (Active-Low)
    input wire pin_LE,     // Latch Enable Input (Active-High / Transparent when High)
    input wire pin_1D,     // Data Input 1
    output reg pin_1Q,     // Data Output 1 (Tri-State)
    input wire pin_2D,     // Data Input 2
    output reg pin_2Q,     // Data Output 2 (Tri-State)
    input wire pin_3D,     // Data Input 3
    output reg pin_3Q,     // Data Output 3 (Tri-State)
    input wire pin_4D,     // Data Input 4
    output reg pin_4Q,     // Data Output 4 (Tri-State)
    input wire pin_5D,     // Data Input 5
    output reg pin_5Q,     // Data Output 5 (Tri-State)
    input wire pin_6D,     // Data Input 6
    output reg pin_6Q,     // Data Output 6 (Tri-State)
    input wire pin_7D,     // Data Input 7
    output reg pin_7Q,     // Data Output 7 (Tri-State)
    input wire pin_8D,     // Data Input 8
    output reg pin_8Q      // Data Output 8 (Tri-State)
);

    reg [7:0] internal_latch; // Internal memory storage representation

    always @(*) begin
        // When LE is high, the latch is transparent (outputs follow inputs)
        if (pin_LE) begin
            internal_latch = {pin_8D, pin_7D, pin_6D, pin_5D, pin_4D, pin_3D, pin_2D, pin_1D};
        end
        
        // Handle Tri-State Output Bus mapping based on OE status
        if (!pin_OE_BAR) begin
            pin_1Q = internal_latch[0];
            pin_2Q = internal_latch[1];
            pin_3Q = internal_latch[2];
            pin_4Q = internal_latch[3];
            pin_5Q = internal_latch[4];
            pin_6Q = internal_latch[5];
            pin_7Q = internal_latch[6];
            pin_8Q = internal_latch[7];
        end else begin
            pin_1Q = 1'bz; pin_2Q = 1'bz; pin_3Q = 1'bz; pin_4Q = 1'bz;
            pin_5Q = 1'bz; pin_6Q = 1'bz; pin_7Q = 1'bz; pin_8Q = 1'bz;
        end
    end

endmodule