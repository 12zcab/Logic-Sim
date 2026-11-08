module mem_2102 (
    input wire pin_CE_BAR,    // Chip Enable Input Control Line (Active-Low)
    input wire pin_R_W_BAR,   // Read/Write Mode Select (High = Read Mode, Low = Write Mode)
    input wire [9:0] pin_A,   // 10-Bit Address Bus (Accesses 1024 discrete single-bit rows)
    input wire pin_DI,        // Dedicated Data Input Pin (Used during write cycles)
    output reg pin_DO         // Dedicated Tri-State Data Output Pin (Used during read cycles)
);

    reg ram_bit_matrix [1023:0]; // 1024 single bits of internal memory storage arrays
    reg internal_bit_holder;

    // Execute synchronous single-bit data write loops
    always @(*) begin
        if (!pin_CE_BAR && !pin_R_W_BAR) begin
            ram_bit_matrix[pin_A] = pin_DI;
        end
    end

    // Evaluate single-bit memory read operations
    always @(*) begin
        if (!pin_CE_BAR && pin_R_W_BAR) begin
            internal_bit_holder = ram_bit_matrix[pin_A];
        end
    end

    // Tri-state buffer separation routing data back out to the digital system
    always @(*) begin
        if (!pin_CE_BAR && pin_R_W_BAR) begin
            pin_DO = internal_bit_holder;
        end else begin
            pin_DO = 1'bz; // Floats the data line to high impedance when disabled
        end
    end

endmodule
