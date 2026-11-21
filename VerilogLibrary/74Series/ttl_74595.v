module IC74595 (
    input        SER,
    input        SRCLK,
    input        SRCLR_BAR
    input        RCLK,
    input        OE_BAR
    output [7:0] Q,
    output       QH_prime
);
    reg [7:0] shift_reg;
    reg [7:0] storage_reg;

    assign QH_prime = shift_reg[7];
    assign Q        = OE_BAR? 8'bzzzzzzzz : storage_reg;

    always @(posedge SRCLK or negedge SRCLR_n) begin
        if (!SRCLR_n)
            shift_reg <= 8'b00000000;
        else
            shift_reg <= {shift_reg[6:0], SER};
    end

    always @(posedge RCLK) begin
        storage_reg <= shift_reg;
    end
endmodule