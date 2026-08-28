//============================================================================
// PS13 Hardware Security — ALU8 Top-Level Wrapper for Nexys A7-100T
//============================================================================
// Module:  alu8_top
// Purpose: Maps physical Nexys A7-100T I/O to the 8-bit ALU.
//
// I/O Mapping:
//   SW[7:0]   → Operand A
//   SW[15:8]  → Operand B
//   BTNU      → OP bit 2   (MSB)
//   BTNL      → OP bit 1
//   BTNR      → OP bit 0   (LSB)
//   BTNC      → not used (reserved)
//   BTND      → not used (reserved)
//   LED[7:0]  → Result Y
//   LED[13]   → Carry flag
//   LED[14]   → Zero flag
//   LED[15]   → Overflow flag
//   LED[12:8] → not used
//   CPU_RESETN → Active-low reset
//   CLK100MHZ  → 100 MHz system clock
//   7-segment  → Hex display of result (optional)
//
// Button-to-Opcode Encoding:
//   No buttons pressed  → 000 (ADD)
//   BTNR only           → 001 (SUB)
//   BTNL only           → 010 (AND)
//   BTNL + BTNR         → 011 (OR)
//   BTNU only           → 100 (XOR)
//   BTNU + BTNR         → 101 (NOT)
//   BTNU + BTNL         → 110 (INC)
//   BTNU + BTNL + BTNR  → 111 (DEC)
//============================================================================

module alu8_top (
    input  wire        CLK100MHZ,    // 100 MHz clock
    input  wire        CPU_RESETN,   // Active-low reset
    input  wire [15:0] SW,           // 16 switches
    input  wire        BTNU,         // Button Up    → OP[2]
    input  wire        BTNL,         // Button Left  → OP[1]
    input  wire        BTNR,         // Button Right → OP[0]
    input  wire        BTNC,         // Button Center (reserved)
    input  wire        BTND,         // Button Down   (reserved)
    output wire [15:0] LED,          // 16 LEDs
    output wire [6:0]  SEG,          // 7-segment segments (active-low: CA-CG)
    output wire        DP,           // 7-segment decimal point (active-low)
    output wire [7:0]  AN            // 7-segment anodes (active-low)
);

    //------------------------------------------------------------------------
    // Internal signals
    //------------------------------------------------------------------------
    wire        rst_n = CPU_RESETN;
    wire [7:0]  op_a  = SW[7:0];     // Operand A from switches
    wire [7:0]  op_b  = SW[15:8];    // Operand B from switches
    wire [2:0]  op_code;             // ALU opcode from buttons
    wire [7:0]  result;              // ALU result
    wire        flag_carry;
    wire        flag_zero;
    wire        flag_overflow;

    //------------------------------------------------------------------------
    // Button-to-Opcode encoding
    // Buttons directly form the 3-bit opcode: {BTNU, BTNL, BTNR}
    //------------------------------------------------------------------------
    assign op_code = {BTNU, BTNL, BTNR};

    //------------------------------------------------------------------------
    // ALU instantiation — Trojan version (contains T1, T2, T3)
    //------------------------------------------------------------------------
    trojan_alu8 u_alu (
        .clk      (CLK100MHZ),
        .rst_n    (rst_n),
        .A        (op_a),
        .B        (op_b),
        .OP       (op_code),
        .Y        (result),
        .carry    (flag_carry),
        .zero     (flag_zero),
        .overflow (flag_overflow),
        .BTNC     (BTNC),
        .BTND     (BTND)
    );

    //------------------------------------------------------------------------
    // LED output mapping
    //------------------------------------------------------------------------
    assign LED[7:0]  = result;        // Result on LEDs 0-7
    assign LED[12:8] = 5'b00000;      // Unused LEDs off
    assign LED[13]   = flag_carry;    // Carry flag
    assign LED[14]   = flag_zero;     // Zero flag
    assign LED[15]   = flag_overflow; // Overflow flag

    //------------------------------------------------------------------------
    // 7-Segment Display — show result in hex on rightmost 2 digits
    //------------------------------------------------------------------------
    // Refresh counter for multiplexing
    reg [19:0] refresh_counter;
    wire [1:0] digit_select;
    reg [3:0]  hex_digit;
    reg [7:0]  anode_mask;

    always @(posedge CLK100MHZ or negedge rst_n) begin
        if (!rst_n)
            refresh_counter <= 20'b0;
        else
            refresh_counter <= refresh_counter + 1;
    end

    assign digit_select = refresh_counter[19:18]; // ~380 Hz refresh per digit

    // Digit multiplexing — only use AN[0] and AN[1] for 2-digit hex
    always @(*) begin
        case (digit_select)
            2'b00: begin
                hex_digit  = result[3:0];   // Lower nibble on digit 0
                anode_mask = 8'b11111110;    // AN[0] active
            end
            2'b01: begin
                hex_digit  = result[7:4];   // Upper nibble on digit 1
                anode_mask = 8'b11111101;    // AN[1] active
            end
            2'b10: begin
                hex_digit  = {1'b0, op_code}; // Opcode on digit 2
                anode_mask = 8'b11111011;    // AN[2] active
            end
            default: begin
                hex_digit  = 4'h0;
                anode_mask = 8'b11111111;    // All off
            end
        endcase
    end

    assign AN = anode_mask;

    // Hex-to-7-segment decoder (active-low segments: CA CB CC CD CE CF CG)
    reg [6:0] seg_data;
    always @(*) begin
        case (hex_digit)
            //                   gfedcba
            4'h0: seg_data = 7'b1000000;
            4'h1: seg_data = 7'b1111001;
            4'h2: seg_data = 7'b0100100;
            4'h3: seg_data = 7'b0110000;
            4'h4: seg_data = 7'b0011001;
            4'h5: seg_data = 7'b0010010;
            4'h6: seg_data = 7'b0000010;
            4'h7: seg_data = 7'b1111000;
            4'h8: seg_data = 7'b0000000;
            4'h9: seg_data = 7'b0010000;
            4'hA: seg_data = 7'b0001000;
            4'hB: seg_data = 7'b0000011;
            4'hC: seg_data = 7'b1000110;
            4'hD: seg_data = 7'b0100001;
            4'hE: seg_data = 7'b0000110;
            4'hF: seg_data = 7'b0001110;
            default: seg_data = 7'b1111111;
        endcase
    end

    assign SEG = seg_data;
    assign DP  = 1'b1;  // Decimal point off (active-low)

endmodule
