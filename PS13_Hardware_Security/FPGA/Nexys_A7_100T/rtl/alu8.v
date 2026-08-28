//============================================================================
// PS13 Hardware Security — Clean 8-bit ALU
//============================================================================
// Module:  alu8
// Purpose: Pure combinational 8-bit ALU — clean reference design (no Trojan).
//          This is the golden reference against which Trojan-infected variants
//          are compared.
//
// Operations (3-bit opcode):
//   000 = ADD    A + B
//   001 = SUB    A - B
//   010 = AND    A & B
//   011 = OR     A | B
//   100 = XOR    A ^ B
//   101 = NOT    ~A
//   110 = INC    A + 1
//   111 = DEC    A - 1
//
// Flags:
//   carry    — carry/borrow out of the 8-bit result
//   zero     — result is zero
//   overflow — signed overflow (2's complement)
//============================================================================

module alu8 (
    input  wire [7:0] A,        // Operand A
    input  wire [7:0] B,        // Operand B
    input  wire [2:0] OP,       // Operation select
    output reg  [7:0] Y,        // Result
    output reg        carry,    // Carry flag
    output reg        zero,     // Zero flag
    output reg        overflow  // Overflow flag (signed)
);

    // Internal 9-bit result for carry detection
    reg [8:0] result_wide;

    always @(*) begin
        // Default values
        result_wide = 9'b0;
        Y           = 8'b0;
        carry       = 1'b0;
        zero        = 1'b0;
        overflow    = 1'b0;

        case (OP)
            3'b000: begin // ADD
                result_wide = {1'b0, A} + {1'b0, B};
                Y           = result_wide[7:0];
                carry       = result_wide[8];
                // Signed overflow: positive + positive = negative, or
                //                  negative + negative = positive
                overflow    = (A[7] == B[7]) && (Y[7] != A[7]);
            end

            3'b001: begin // SUB
                result_wide = {1'b0, A} - {1'b0, B};
                Y           = result_wide[7:0];
                carry       = result_wide[8]; // Borrow
                // Signed overflow: positive - negative = negative, or
                //                  negative - positive = positive
                overflow    = (A[7] != B[7]) && (Y[7] != A[7]);
            end

            3'b010: begin // AND
                Y = A & B;
            end

            3'b011: begin // OR
                Y = A | B;
            end

            3'b100: begin // XOR
                Y = A ^ B;
            end

            3'b101: begin // NOT (unary, operates on A only)
                Y = ~A;
            end

            3'b110: begin // INC (A + 1)
                result_wide = {1'b0, A} + 9'b1;
                Y           = result_wide[7:0];
                carry       = result_wide[8];
                overflow    = (~A[7]) && (Y[7]); // 0x7F + 1 = 0x80
            end

            3'b111: begin // DEC (A - 1)
                result_wide = {1'b0, A} - 9'b1;
                Y           = result_wide[7:0];
                carry       = result_wide[8]; // Borrow
                overflow    = (A[7]) && (~Y[7]); // 0x80 - 1 = 0x7F
            end

            default: begin
                Y = 8'b0;
            end
        endcase

        // Zero flag — common to all operations
        zero = (Y == 8'b0);
    end

endmodule
